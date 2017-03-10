from flask import Flask
from flask import request
from flask import jsonify
from flask.ext.mysql import MySQL
import ast
from oorjan.data.models import Datapoints, ReferenceData, SolarSysMetadata, db
from datetime import datetime

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1111'
app.config['MYSQL_DATABASE_DB'] = 'SOLAR_DATA'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1111@localhost/SOLAR_DATA'
mysql.init_app(app)
db.init_app(app)


@app.route("/")
def index():
    return "Index!"


@app.route("/ping", methods=['GET', ])
def health_check():
    data = SolarSysMetadata.query.get(3)
    print data.system_capacity
    return 'OLA'

'''
@app.route("/api/v1/<solar_system_id>", methods=['GET', ])
def compare_dc_power(solar_system_id):
    date = request.args.get('date')
    day, month, year = date.split('-')
    date = "{0}-{1}-{2}".format(year, month, day)
    conn = mysql.connect()
    cursor = conn.cursor()
    query1 = "SELECT * from datapoints WHERE date >= '{0} 01:00:0' AND date <= '{1} 23:59:0' AND system_identifier = {2}".format(
        date, date, solar_system_id)
    cursor.execute(query1)
    data = cursor.fetchall()
    query2 = "SELECT * from reference_data where day={0} AND month={1} AND system_capacity={2}".format(
        day, month, solar_system_id)
    cursor.execute(query2)
    reference_data = cursor.fetchone()
    dd = ast.literal_eval(reference_data[2])
    result = []
    for index, row in enumerate(data):
        print row[1]
        print dd[index]
        if row[1] < (dd[index] * 0.8):
            result.append(1)
        else:
            result.append(0)
    return jsonify(result)
'''


@app.route("/api/v1/<solar_system_id>", methods=['GET', ])
def compare_dc_power(solar_system_id):
    date = request.args.get('date')
    day, month, year = date.split('-')
    date_1 = "{0}-{1}-{2}".format(year, month, day)
    date1 = date + ' 01:00:0'
    date2 = date + ' 23:59:0'
    date1 = datetime.strptime(date1, "%d-%m-%Y %H:%M:%S")
    date2 = datetime.strptime(date2, "%d-%m-%Y %H:%M:%S")
    data = Datapoints.query.filter(Datapoints.date.between(date1, date2))
    ref_data = ReferenceData.query.filter(ReferenceData.day == day, ReferenceData.month==month, ReferenceData.system_capacity==solar_system_id).first() 
    dd=ast.literal_eval(ref_data.datapoints)
    result=[]
    print data
    i = 0
    for row in data:
        print row.dc_solar_power
        print dd[i]
        if row.dc_solar_power < (dd[i] * 0.8):
            result.append(1)
        else:
            result.append(0)
        i += 1
    return jsonify(result)

@app.route("/api/v1/solar_data/<system_id>", methods=['POST', ])
def upload_solar_data(system_id):
    json_data=request.get_json()
    solar_data = Datapoints(dc_solar_power=json_data['dc_solar_power'], date=json_data['date'], system_identifier=system_id)
    db.session.add(solar_data)
    db.session.commit()
    return 'as'

'''
@app.route("/api/v1/solar_data/<system_id>", methods=['POST', ])
def upload_solar_data(system_id):
    json_data=request.get_json()
    print json_data
    print system_id
    conn=mysql.connect()
    cursor=conn.cursor()
    query="INSERT INTO datapoints (dc_solar_power, date, system_identifier) VALUES({0}, '{1}', {2})".format(
        json_data['dc_solar_power'], json_data['date'], system_id)
    cursor.execute(query)
    conn.commit()
    return 'as'
'''

if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(debug=True)
