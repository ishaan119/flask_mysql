from datetime import datetime


def validate_date(date):
    try:
        date1 = date + ' 01:00:00'
        date2 = date + ' 23:59:00'
        date1 = datetime.strptime(date1, '%d-%m-%Y %H:%M:%S')
        date2 = datetime.strptime(date2, '%d-%m-%Y %H:%M:%S')
        return (date1, date2)
    except ValueError:
        return False, False


def job1(t, j):
    print 'DOne'


'''
def job1(t, j):
    logging.basicConfig()
    msg = Message('Hello', sender='ishaansutaria@gmail.com',
                  recipients=['ishaansutaria@gmail.com'])
    msg.body = 'Hsad'
    with app.app_context():
        mail.send(msg)
    print 'mail sent'
'''
