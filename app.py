from flask import Flask
from flask import request
from flask import jsonify
from flask.ext.mysql import MySQL
import ast


mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1111'
app.config['MYSQL_DATABASE_DB'] = 'SOLAR_DATA'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def index():
    return "Index!"


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


@app.route("/api/v1/solar_data/<system_id>", methods=['POST', ])
def upload_solar_data(system_id):
    json_data = request.get_json()
    print json_data
    print system_id
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "INSERT INTO datapoints (dc_solar_power, date, system_identifier) VALUES({0}, '{1}', {2})".format(
        json_data['dc_solar_power'], json_data['date'], system_id)
    cursor.execute(query)
    conn.commit()
    return 'as'


if __name__ == "__main__":
    app.run(debug=True)
