import csv
from datetime import datetime
import logging
import matplotlib.pyplot as plt
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pytz
import requests
import slack_data
import speedtest
import sys
import time

################################################################################
# This is the main function that will run the network speed test.
# It will create the log directory, and log the results
# of the test in csv format with filename: ./logs/network_data_<date>.
# Input: path, filename, date, slack_url
# Output: None
################################################################################
def main(path, filename, date, slack_url):

    #Init variables
    downloads = []
    uploads = []
    json_obj = {}

    #Check if the network_data_<date> file already exists, if not, make it
    if not os.path.exists(os.path.expanduser(path)):
        #Create file and add headers
        with open(os.path.expanduser(path + filename + date),'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(zip(["Download(Mb/s)"],
                                 ["Upload(Mb/s)"],
                                 ["TimeStamp"]))

    try:
		#Run the network speed test
        download, upload = get_speedtest_results()

        send_slack_update(slack_url, download, upload)

        if not os.path.exists(os.path.expanduser(path)):
            #Write the results of the test to the log
            with open(os.path.expanduser(path + filename + date), 'a',  newline='') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerows(zip([download],
                                     [upload],
                                     [current_time]))

    except:
        handle_exception(slack_url)


################################################################################
# This function produces the current date and time to be used for logging
# purposes.
# Input: None
# Output: date, current_time
################################################################################
def get_date_time():
    d = datetime.now(pytz.timezone('US/Central'))
    date = d.strftime('%m-%d-%Y')
    current_time = d.strftime('%H:%M:%S')
    return date, current_time



################################################################################
# Sends the results of the test to the slack API.
# Input: None
# Output: date, current_time
################################################################################
def send_slack_update(url, download, upload):
    json_obj = {
    'text': 'Speed test results: {} {}'.format(download, upload)
    }
    response = requests.post(url, json=json_obj)

def send_slack_exception(url, exception, filename, line_number):
    json_obj={'text': 'An exception occured: {} in {} on line {}'.format(exception, filename, line_number)}
    response = requests.post(url, json=json_obj)

def handle_exception(slack_url):
    err_type, err_object, err_trace = sys.exc_info()

    err_name = err_type.__name__
    err_filename = err_trace.tb_frame.f_code.co_filename
    line_number = err_trace.tb_lineno

    send_slack_exception(slack_url, err_name, filename, line_number)

def upload_file_to_google_drive():
    # gauth = GoogleAuth()
    # gauth.LocalWebserverAuth()
    # drive = GoogleDrive(gauth)
    pass



################################################################################
# This function performs the speed test for download and upload speeds.
# It then formats the results in Megabits/second and returns them.
# Input: None
# Output: download, upload
################################################################################
def get_speedtest_results():

    #Create speedtest object
    speedtester = speedtest.Speedtest()

    #Call download and upload function to retrieve data
    download = speedtester.download()
    upload = speedtester.upload()

    #Reformat the data to Mb and round to two decimal places
    download = round(download/10**6, 2)
    upload = round(upload/10**6, 2)

    return download, upload


def plot_data(path, filename, date, slack_url):
    time = []
    download = []
    upload = []

    try:
        with open(os.path.expanduser(path + filename + date), 'r') as file:
            data = csv.reader(file, delimiter='\t')

            #Skip the header
            next(data)

            for row in data:
                download.append(float(row[0]))
                upload.append(float(row[1]))
                time.append(row[2])


        fig = plt.figure('Network Speeds vs. Time')
        ax = fig.add_subplot(111)

        ax.scatter(time, download, s=10, c='b', marker="s", label='Download')
        ax.scatter(time, upload, s=10, c='r', marker="o", label='Upload')
        fig.legend()

        plt.xlabel('Time (H:M:S)')
        plt.ylabel('Speed (Mbps)')
        plt.title('Download and Upload Speeds vs. Time')
        plt.savefig(os.path.expanduser(path) + 'plot_{}'.format(date))

    except:
        handle_exception(slack_url)


################################################################################
# Usage function to detail where the results of this script can be found and
# indicate dependencies.
# Input: None
# Output: download, upload
################################################################################
#TODO: Update usage string
def usage():
    usage_string = '''\nThis script will test your network download and upload speeds.
The output can be found in ./logs/network_data_{date_it_was_run}.csv.
A detailed logging history can be seen in ./logs/speed_test_main_debug_{date_it_was_run}.log\n
This script requires that 'speedtest.py' be in the same directory when running the script.\n'''
    print(usage_string)


if __name__ == '__main__':

    #init data
    path = '~/logs/network_data_logs/'
    filename = 'network_data_'
    slack_url = slack_data.get_slack_url()
    date, current_time = get_date_time()

    #Check if the logs/ folder already exists, if not, make it
    if not os.path.exists(os.path.expanduser(path)):
        os.makedirs(os.path.expanduser(path))

    main(path, filename, date, slack_url)
    plot_data(path, filename, date, slack_url)
