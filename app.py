from flask import Flask, request, jsonify
from FnoSpreadSheet import get_r1_s1_values, end_of_the_sheet
from processFile import process_data
from flask_cors import CORS, cross_origin
from datetime import datetime, time
from time import sleep
import pytz
import logging
import threading

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['TIMEOUT'] = 600
get_stocks = False
thread = None
lock = threading.Lock()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def start_process():
    global get_stocks
    r1s1_df = get_r1_s1_values()
    while get_stocks:
        try:
            process_data(r1s1_df)
            sleep(30)
        except Exception as e:
            logger.error(f"Error in processing data: {e}")

@app.route('/update_status', methods=['POST'])
def update_status():
    global get_stocks, thread
    status = request.form.get('status')
    if status.lower() == 'true' and not get_stocks:
        with lock:
            get_stocks = True
            thread = threading.Thread(target=start_process)
            thread.start()
            logger.info("Process started.")
        return jsonify({'status': 'Process started.'}), 200
    elif status.lower() == 'false' and get_stocks:
        with lock:
            get_stocks = False
            if thread:
                thread.join()
            logger.info("Process stopped.")
        return jsonify({'status': 'Process stopped.'}), 200
    elif status.lower() == 'false' and not get_stocks:
        return jsonify({'status': 'Process is not running.'}), 200
    return jsonify({'status': 'Process is already running.'}), 200

@app.route('/update_previous_sheet', methods=['POST'])
@cross_origin()
def update_previous_sheet():
    ist_timezone = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist_timezone)
    current_weekday = now.weekday()
    current_time = now.time()
    start_time = time(9, 10)
    end_time = time(16, 0)
    logger.info(f"Current time: {current_time}, Weekday: {current_weekday}")
    if (current_weekday not in [5, 6] and (current_time <= start_time or current_time >= end_time)):
        try:
            end_of_the_sheet()
            return jsonify({'status': 'Sheet Updated Successfully'}), 200
        except Exception as e:
            logger.error(f"Error updating sheet: {e}")
            return jsonify({'status': 'Error updating sheet'}), 500
    else:
        return jsonify({'status': 'Market is now live, cannot update the sheet'}), 400

@app.route('/get_status', methods=['GET'])
def get_status():
    global get_stocks
    return jsonify({'status': get_stocks}), 200

@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'
