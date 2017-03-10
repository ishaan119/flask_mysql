from datetime import datetime
from flask import jsonify

def validate_date(date):
    try:
        date1 = date + ' 01:00:00'
        date2 = date + ' 23:59:00'
        date1 = datetime.strptime(date1, '%d-%m-%Y %H:%M:%S')
        date2 = datetime.strptime(date2, '%d-%m-%Y %H:%M:%S')
        return (date1, date2)
    except ValueError:
        return False, False
