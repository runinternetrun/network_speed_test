import schedule
import speedtest
import sys
import time
import threading


################################################################################
# This is the main function that will run the speed test and report the results
# Input: None
# Output: None
################################################################################
def main():

    #Init variables
    downloads = 0
    uploads = 0

    try:
		#Run the network speed test
        download, upload = get_speedtest_results()
        print('Download: {}    Upload: {}    Time: {}'.format(download, upload, time.ctime()))

    except:
        handle_exception()

def handle_exception():
    err_type, err_object, err_trace = sys.exc_info()

    err_name = err_type.__name__
    err_filename = err_trace.tb_frame.f_code.co_filename
    line_number = err_trace.tb_lineno

    print('Error: {} occurred in {} on line {}'.format(err_name, err_filename, line_number))

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

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

if __name__ == '__main__':

    schedule.every(30).seconds.do(run_threaded, main)

    while True:
        try:
            schedule.run_pending()
        except:
            handle_exception()
        time.sleep(1)
    # main()
