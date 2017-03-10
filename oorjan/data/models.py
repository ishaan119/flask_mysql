from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Datapoints(db.Model):
    id_datapoints = db.Column(db.Integer, primary_key=True)
    dc_solar_power = db.Column(db.DECIMAL)
    date = db.Column(db.DateTime)
    system_identifier = db.Column(db.Integer, db.ForeignKey(
        'solar_sys_metadata.system_capacity'))


class ReferenceData(db.Model):
    idreference_data = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    datapoints = db.Column(db.VARCHAR(200))
    month = db.Column(db.Integer)
    system_capacity = db.Column(db.Integer, db.ForeignKey(
        'solar_sys_metadata.system_capacity'))



class SolarSysMetadata(db.Model):
    tilt = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    lon = db.Column(db.Integer)
    dataset = db.Column(db.VARCHAR(45))
    array_type = db.Column(db.Integer)
    module_type = db.Column(db.Integer)
    azimuth = db.Column(db.Integer)
    lat = db.Column(db.Integer)
    system_capacity = db.Column(db.Integer, primary_key=True)
    timeframe = db.Column(db.VARCHAR(45))

    def __init__(self, tilt, losses, lon, dataset, array_type, module_type,
                 azimuth, lat, system_capacity, timeframe):
        self.system_capacity = system_capacity
        self.losses = losses
        self.tilt = tilt
        self.lon = lon
        self.dataset = dataset
        self.array_type = array_type
        self.module_type = module_type
        self.azimuth = azimuth
        self.lat = lat
        self.timeframe = timeframe
