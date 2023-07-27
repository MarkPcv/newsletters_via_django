import datetime


def my_scheduled_job():
    message = str(datetime.datetime.now()) + ': Hi there\n'
    with open('/Users/markpcv/Desktop/test/test.txt', 'a') as f:
        f.write(message)

