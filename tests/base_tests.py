import os
import sys
import datetime
# topdir = os.path.join(os.path.dirname(__file__), "..")
# sys.path.append(topdir)
sys.path.append("..")
import unittest
 
from oorjan import app, db
from oorjan.data.models import Datapoints, ReferenceData, SolarSysMetadata

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'test.db')
print DATABASE
TEST_DB = 'test.db'
 
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
        self.app = app.test_client()
        with app.test_request_context():
            db.drop_all()
            db.create_all()
            # Adding seed data
            # Adding metadata
            meta_data = SolarSysMetadata(28, 10, 77, 'IN', 1, 1, 180, 28, 3, 'hourly')
            db.session.add(meta_data)
            # Adding reference data 
            ref_data = ReferenceData(day=1,datapoints='(0,0,0,0,0,0,0,318.475,2489.115,4396.037,5645.406,6535.4,7011.977,6864.036,6429.069,4976.679,3135.839,885.004,0,0,0,0,0,0)', month=1, system_capacity=10)
            db.session.add(ref_data)
            # Adding 24 Datapoints for a single Day of Datapoints
            day, month, year = 06, 01, 2016
            date = datetime.datetime.combine( datetime.date(year, month, day), datetime.time(0, 0))
            datapoints = [0,0,0,0,0,0,0,180,270,600, 600, 630,750, 930, 900, 1110, 1100, 810, 0 ,0 ,0 ,0 ,0 , 0]
            for index, i in enumerate(datapoints):
                if index == 23:
                    date = date + datetime.timedelta(minutes=59)
                else:
                    date = date + datetime.timedelta(hours=1)
                datapoints_data = Datapoints(dc_solar_power=i, date=date, system_identifier=3)
                db.session.add(datapoints_data)

            db.session.commit()
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
 
    ###############
    #### tests ####
    ###############
 
    def test_main_page(self):
        response = self.app.get('/apiv1/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_heath_check(self):
        response = self.app.get('/apiv1/ping', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_upload_solar_data(self):
        post_data = dict(dc_solar_power=0, date='2015-01-21 01:00:00')
        response = self.app.post('/apiv1/solar_data/3',
                                 data =dict(dc_solar_power=0, date='2015-01-21 01:00:00'),
                                 headers={'Content-Type': 'application/json'},
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 201)

    def test_compare_dc_power(self):
        pass




 
 
if __name__ == "__main__":
    unittest.main()