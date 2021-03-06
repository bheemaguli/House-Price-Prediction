from housing.logger import logging
from housing.exception import HousingException
from housing.config.config import Configuartion
from housing.constant import CONFIG_DIR, get_current_time_stamp
from housing.pipeline.pipeline import Pipeline
from housing.entity.housing_predictor import HousingPredictor, HousingData
from housing.util.util import read_yaml_file, write_yaml_file

from flask import Flask, render_template, url_for, redirect, request, \
    send_file, abort
from flask_bootstrap import Bootstrap5
from matplotlib.style import context
import os, sys
import sys
import ast

ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "housing"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)
HOUSING_DATA_KEY = "housing_data"
MEDIAN_HOUSING_VALUE_KEY = "median_house_value"

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)

@app.route('/roadmap', methods=['GET'])
def roadmap():
    return render_template('roadmap.html')

@app.route('/data', methods=['GET'])
def data():
    return render_template('data.html')

@app.route('/eda', methods=['GET'])
def eda():
    return render_template('eda.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', e=e)

@app.route('/artifact', defaults={'req_path': 'housing'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs("housing", exist_ok=True)
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)

@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    pipeline = Pipeline(config=Configuartion(current_time_stamp=get_current_time_stamp()))
    experiment_df = pipeline.get_experiments_status()
    context = {
        "experiment": list(experiment_df.itertuples(index=False, name=None))
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(config=Configuartion(current_time_stamp=get_current_time_stamp()))
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        HOUSING_DATA_KEY: None,
        MEDIAN_HOUSING_VALUE_KEY: None
    }

    if request.method == 'POST':
        longitude = float(request.form['longitude'])
        latitude = float(request.form['latitude'])
        housing_median_age = float(request.form['housing_median_age'])
        total_rooms = float(request.form['total_rooms'])
        total_bedrooms = float(request.form['total_bedrooms'])
        population = float(request.form['population'])
        households = float(request.form['households'])
        median_income = float(request.form['median_income'])
        ocean_proximity = request.form['ocean_proximity']

        housing_data = HousingData(longitude=longitude,
                                   latitude=latitude,
                                   housing_median_age=housing_median_age,
                                   total_rooms=total_rooms,
                                   total_bedrooms=total_bedrooms,
                                   population=population,
                                   households=households,
                                   median_income=median_income,
                                   ocean_proximity=ocean_proximity,
                                   )
        housing_df = housing_data.get_housing_input_data_frame()
        housing_predictor = HousingPredictor(model_dir=MODEL_DIR)
        median_housing_value = housing_predictor.predict(X=housing_df)
        context = {
            HOUSING_DATA_KEY: housing_data.get_housing_data_as_dict(),
            MEDIAN_HOUSING_VALUE_KEY: median_housing_value,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        return send_file(abs_path)

    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models.html', result=result)


@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        message = ""
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.strip()
            model_config = model_config.replace("'", '"')
            if len(model_config) > 0:
                try:
                    model_config = ast.literal_eval(model_config)
                    message = "Model configuration updated successfully."
                    write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)
                except:
                    message = "Model configuration is invalid."
            else:
                message = "No model configuration input was given."
            print(model_config)


        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config}, message=message)

    except  Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    if not os.path.exists(abs_path):
        return abort(404)

    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('logs.html', result=result)
    
if __name__ == '__main__':
    app.run()