import csv
from datetime import datetime
import logging
import matplotlib.pyplot as plt
import os
import pytz
import requests
import slack_data
import speedtest
import sys
import time



################################################################################
# This is the main function that will run the network speed test.
# It will create the log directory, set up the debug logger, and log the results
# of the test in csv format with filename: ./logs/network_data_<date>.csv.
# The debug log file can be found at: ./logs/speed_test_main_debug_<date>.log
# Input: None
# Output: None
################################################################################
def main(path, filename, date):

    #Init variables
    downloads = []
    uploads = []

    slack_url = slack_data.get_slack_url()
    json_obj = {}

    #Check if the network_data_<date> file already exists, if not, make it
    if not os.path.exists(os.path.expanduser(path)):

        #Create file and add headers
        with open(os.path.expanduser(path + filename + date),'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(zip(["Download(Mb/s)"],
                                 ["Upload(Mb/s)"],
                                 ["TimeStamp"]))

    # logger = logging.getLogger()
    # logger.info("Starting test...")

    try:
		#Run the network speed test
        download, upload = get_speedtest_results()
        # logging.info("Download: {}   Upload: {}".format(download, upload))

        json_obj={'text':'Speed Test: \n     Download: {} Mbps \n     Upload: {} Mbps'.format(download, upload)}

        send_slack_update(slack_url, json_obj)

        #Write the results of the test to the log
        with open(os.path.expanduser(path + filename + date), 'a',  newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(zip([download],
                                 [upload],
                                 [current_time]))

    except:
        err = sys.exc_info()
        # logging.exception("An exception occured: {}".format(err[0].__name__))
        # print("An exception occured: {}".format(err[0].__name__))
        json_obj={'text':'An exception occured: {}'.format(err[0].__name__)}
        send_slack_update(slack_url, json_obj)

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
def send_slack_update(url, json_obj):
    response = requests.post(url, json=json_obj)



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


def plot_data(path, filename, date):
    time = []
    download = []
    upload = []

    with open(os.path.expanduser(path + filename + date), 'r') as file:
        data = csv.reader(file, delimiter='\t')

        #Skip the header
        next(data)

        for row in data:
            # print(row)
            download.append(float(row[0]))
            upload.append(float(row[1]))
            time.append(row[2])


    fig = plt.figure('Network Speeds vs. Time')
    ax = fig.add_subplot(111)

    ax.scatter(time, download, s=10, c='b', marker="s", label='Download')
    ax.scatter(time, upload, s=10, c='r', marker="o", label='Upload')
    fig.legend()

    plt.xlabel('Time')
    plt.ylabel('Mbps')
    plt.title('Download and Upload Speeds vs. Time')
    plt.savefig(os.path.expanduser(path) + 'plot_{}'.format(date))
    # print(download, upload, time)




################################################################################
# Usage function to detail where the results of this script can be found and
# indicate dependencies.
# Input: None
# Output: download, upload
################################################################################
def usage():
    usage_string = '''\nThis script will test your network download and upload speeds.
The output can be found in ./logs/network_data_{date_it_was_run}.csv.
A detailed logging history can be seen in ./logs/speed_test_main_debug_{date_it_was_run}.log\n
This script requires that 'speedtest.py' be in the same directory when running the script.\n'''
    print(usage_string)


if __name__ == '__main__':

    path = '~/logs/network_data_logs/'
    filename = 'network_data_'

    #Get the current date and time
    date, current_time = get_date_time()

    #Check if the logs/ folder already exists, if not, make it
    if not os.path.exists(os.path.expanduser(path)):
        os.makedirs(os.path.expanduser(path))

    #Create the debug logger
    # filename = os.path.expanduser('~/logs/network_data_logs/speed_test_main_debug_{}.log'.format(date))
    # log_format = '%(levelname)s %(asctime)s - %(message)s'
    # logging.basicConfig(filename=filename,
    #                    level   =logging.DEBUG,
    #                    format  =log_format)
    # usage()

    main(path, filename, date)
    plot_data(path, filename, date)
