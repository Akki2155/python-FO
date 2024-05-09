from flask import Flask, request, jsonify
from FnoSpreadSheet import get_r1_s1_values
import threading
from processFile import process_data
from time import sleep
from FnoSpreadSheet import end_of_the_sheet
from datetime import datetime, time
from flask_cors import CORS,cross_origin
import pytz

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['TIMEOUT'] = 600
get_stocks = False
thread = None

def start_process():
    global get_stocks
    r1s1_df=get_r1_s1_values()
    while get_stocks:
        process_data(r1s1_df)
        sleep(30)

@app.route('/update_status', methods=['POST'])
def update_status():
    global get_stocks, thread
    status = request.form.get('status')
    if status.lower() == 'true' and not get_stocks:
        get_stocks = True
        # Start the process in a new thread
        thread = threading.Thread(target=start_process)
        thread.start()
        return jsonify({'status': 'Process started.'}), 200
    elif status.lower() == 'false' and get_stocks:
        get_stocks = False
        # Join the thread to stop the process gracefully
        if thread:
            thread.join()
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
    print(current_time, current_time<=start_time, current_time>=end_time)
    # holiday_calendra=process_holiday_calendra()
    if (current_weekday not in [5, 6] and (current_time<=start_time or current_time>=end_time)):
              
            end_of_the_sheet()
            return jsonify({'status': 'Sheet Updated Successfully'}), 200
    else:
        return jsonify({'status': 'Market is now live, cannot update the sheet'}), 400


@app.route('/get_status', methods=['GET'])
def get_status():
    global get_stocks
    return jsonify({'status': get_stocks}), 200

@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'

