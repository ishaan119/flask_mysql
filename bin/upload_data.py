import random
import datetime
import requests


def get_dc_power(system_capacity, start_range, end_range):
    dc_percent = random.randint(start_range, end_range)
    return (dc_percent / float(100)) * (system_capacity * 1000)


def generate_load_data(system_capacity):
    data = []
    # For loop till 1pm where at 1pm the
    # system capacity will be in the range of
    # 85% - 95% to have some variable data creation
    for i in range(24):
        if i == 7 or i == 8:
            data.append(get_dc_power(system_capacity, 5, 10))
        elif i == 9 or i == 10:
            data.append(get_dc_power(system_capacity, 10, 20))
        elif i == 11 or i == 12:
            data.append(get_dc_power(system_capacity, 20, 30))
        elif i == 13 or i == 14:
            data.append(get_dc_power(system_capacity, 30, 40))
        elif i == 15 or i == 16:
            data.append(get_dc_power(system_capacity, 30, 40))
        elif i == 17:
            data.append(get_dc_power(system_capacity, 20, 30))
        else:
            data.append(0.0)
    print data
    print len(data)
    return data


def upload_solar_perf_data(system_capacity, date):
    data = generate_load_data(system_capacity)
    day, month, year = map(int, date.split('-'))
    date = datetime.datetime.combine(
        datetime.date(year, month, day), datetime.time(0, 0))
    upload_url = 'http://localhost:5000/apiv1/solar_data/{0}'.format(system_capacity)
    for index, i in enumerate(data):
        if index == 23:
            date = date + datetime.timedelta(minutes=59)
        else:
            date = date + datetime.timedelta(hours=1)
        post_data = {'dc_solar_power': i, 'date': str(date)}
        r = requests.post(upload_url, json=post_data)
        print r


upload_solar_perf_data(222, '23-01-2015')
