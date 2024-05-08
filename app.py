from flask import Flask, request, jsonify
from FnoSpreadSheet import get_r1_s1_values
import threading
from processFile import process_data, process_holiday_calendra
from time import sleep
from FnoSpreadSheet import end_of_the_sheet
from datetime import datetime

app = Flask(__name__)
get_stocks = False
thread = None

def start_process():
    global get_stocks
    r1s1_df=get_r1_s1_values()
    while get_stocks:
        process_data(r1s1_df)
        sleep(60)

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
def update_previous_sheet():
    now = datetime.now()
    current_weekday = now.weekday()
    current_time = now.time()
    print(current_time)
    date=now.date
    holiday_calendra=process_holiday_calendra()
    if (
        date not in holiday_calendra and current_weekday not in [5, 6] and
        (current_time <= datetime.strptime('09:10', '%H:%M').time() or
        current_time >= datetime.strptime('16:00', '%H:%M').time())):
            
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

