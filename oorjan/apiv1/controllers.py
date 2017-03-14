from flask import Blueprint, current_app
from flask import request
from flask import jsonify
import ast
from oorjan.data.models import Datapoints, ReferenceData, SolarSysMetadata, db
from datetime import datetime
from oorjan.utils import validate_date

apiv1 = Blueprint('apiv1', __name__)

@apiv1.route("/")
def index():
    return "Index!"


@apiv1.route("/ping", methods=['GET', ])
def health_check():
    data = SolarSysMetadata.query.get(3)
    print data.system_capacity
    return '', 200


@apiv1.route("/<solar_system_id>", methods=['GET', ])
def compare_dc_power(solar_system_id):
    date = request.args.get('date')
    day, month, year = date.split('-')
    date1, date2 = validate_date(date)
    # If the Date is not in the valid format
    if date1 is False:
        current_app.logger.error('Invalid Date Received:' + date)
        response = jsonify({'message': 'This Date is not in the correct format. It should be DD-MM-YYYY'})
        response.status_code = 400
        return response
    data = Datapoints.query.filter(Datapoints.date.between(date1, date2)).all()
    # Test if the date has all 24 Datapoints for 24 hours
    if len(data) != 24:
        current_app.logger.error('Length of datapoints received:' + str(data))
        response = jsonify({'message':'This Date does not have all 24 datapoints'})
        response.status_code = 404 
        return response

    # The .one() call makes sure we only get one row of datapoints for a particular system_capacity
    ref_data = ReferenceData.query.filter(ReferenceData.day == day, ReferenceData.month==month, ReferenceData.system_capacity==solar_system_id).one() 
    dd=ast.literal_eval(ref_data.datapoints)
    result = []
    current_app.logger.debug('Reference Data' + ref_data.datapoints)
    i = 0
    for row in data:
        print row.dc_solar_power
        print dd[i]
        if row.dc_solar_power < (dd[i] * 0.8):
            result.append(1)
        else:
            result.append(0)
        i += 1
    response = jsonify(result)
    response.status_code = 200
    return response


@apiv1.route("/solar_data/<system_id>", methods=['POST', ])
def upload_solar_data(system_id):
    json_data = request.get_json()
    # //Todo Validate Json Schema
    # Check if System Id is valid
    solar_system_info = SolarSysMetadata.query.get(system_id)
    if solar_system_info is None:
        response = jsonify({'message': 'The system id not found'})
        response.status_code = 404
        return response
    current_app.logger.info('Uploading Solar Data for solar_system:' + system_id)
    current_app.logger.info(json_data)
    solar_data = Datapoints(dc_solar_power=json_data['dc_solar_power'], date=json_data['date'], system_identifier=system_id)
    db.session.add(solar_data)
    db.session.commit()
    return '', 201
