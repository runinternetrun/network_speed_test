import csv
from datetime import datetime
import logging
import os
import pytz
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
def main():
    #Init variables
    downloads = []
    uploads = []
    # t = 0
    sleep_interval = 5

    #Get the current date and time
    date, current_time = get_date_time()

    #Check if the logs/ folder already exists, if not, make it
    if not os.path.exists('./logs'):
        os.makedirs('./logs')

    #Check if the network_data_<date> file already exists, if not, make it
    if not os.path.exists("./logs/network_data_{}.csv".format(date)):

        #Create file and add headers
        with open("./logs/network_data_{}.csv".format(date),'w') as speed_data:
            writer = csv.writer(speed_data, delimiter='\t')
            writer.writerows(zip(["Download (Mb/s)"],
                                 ["Upload (Mb/s)"],
                                 ["Time Stamp"]))

    #Create the debug logger
    # filename = './logs/speed_test_main_debug_{}.log'.format(date)
    # log_format = '%(levelname)s %(asctime)s - %(message)s'
    # logging.basicConfig(filename=filename,
    #                     level   =logging.DEBUG,
    #                     format  =log_format)

    # logger = logging.getLogger()
    # logger.info("Starting test...")

    try:
		#Run the network speed test
        download, upload = get_speedtest_results()

        logging.info("Download: {}   Upload: {}".format(download, upload))

        #Write the results of the test to the log
        with open("./logs/network_data_{}.csv".format(date),'a') as speed_data:
            writer = csv.writer(speed_data, delimiter='\t')
            writer.writerows(zip([download],
                                 [upload],
                                 [current_time]))
    except:
        err = sys.exc_info()
        print("An error has occured {err[0].__name__}")
        # logging.exception("An exception occured: {}".format(err[0].__name__))



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
    # usage()
    main()
