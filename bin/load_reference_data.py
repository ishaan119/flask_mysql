import requests
import MySQLdb


def download_data(lat, lon, system_capacity):
    base_url = 'https://developer.nrel.gov/api/pvwatts/v5.json'
    payload = {'api_key': 'DEMO_KEY', 'lat': lat, 'lon': lon,
               'system_capacity': system_capacity, 'azimuth': 180,
               'tilt': 19, 'array_type': 1, 'module_type': 1,
               'losses': 10, 'dataset': 'IN', 'timeframe': 'hourly'}
    r = requests.get(base_url, params=payload)
    print r.url
    raw_data = r.json()
    metadata, dc_data = raw_data['inputs'], raw_data['outputs']['dc']
    print metadata
    print len(dc_data)
    dc_data = split_list(dc_data, 365)
    print len(dc_data)
    return metadata, dc_data


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


def insert_ref_to_db(query, execute_many=False, data=[]):
    db = MySQLdb.connect(host="127.0.0.1", user="root",
                         passwd="1111", db="SOLAR_DATA")

    cur = db.cursor()
    # cur.execute("select * from reference_data")
    print query
    print data[0]
    if execute_many:
        cur.executemany(query, data)
    else:
        cur.execute(query)
    db.commit()
    db.close()


def add_solar_sys_metadata(system_capacity, lat, lon):
    data = (lat, 10, lon, 'IN', 1, 1, 180, lat, system_capacity, "hourly")
    sql = "INSERT INTO solar_sys_metadata (tilt, losses, lon, dataset, array_type, module_type, azimuth, lat, system_capacity, timeframe) VALUES(%s, %s, %s, '%s', %s, %s, %s, %s, %s,'%s')" % data
    insert_ref_to_db(sql)


def add_reference_data(system_capacity, lat, lon):
    metadata, dc_data = download_data(lat, lon, system_capacity)
    months_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dc_count = 0
    assert sum(months_days) == 365
    sql_data = []
    for index, days in enumerate(months_days):
        for i in range(days):
            sql_data.append(
                (i + 1, dc_data[dc_count], index + 1, system_capacity))
            dc_count += 1
    print dc_count
    sql_query = "INSERT INTO reference_data (day, datapoints, month,system_capacity) VALUES(%s, '%s', %s, %s)"
    insert_ref_to_db(sql_query, True, sql_data)


# download_data(19, 73, 10)
# download_data(19, 73, 10)
# download_data(19, 73, 3)
# add_solar_sys_metadata(10, 19, 73)
# add_solar_sys_metadata(3, 28, 77)
add_reference_data(3, 28, 77)
