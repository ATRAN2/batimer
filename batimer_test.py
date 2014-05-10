import unittest
import batimer
import datetime
from batimer import Status, db
import sqlalchemy

class BatimerTest(unittest.TestCase):
	def test_batimer_has_date(self):
		app = batimer.app.test_client()
		response = app.get('/')
		self.assertIn('form', response.data,)

	def test_batimer_posts_data(self):
		app = batimer.app.test_client()
		response = app.post('/', 
			data={
				'testpost' : 'test',
			}
		)
		self.assertIn('', response.data)

	def test_batimer_can_use_post_dates(self):
		app = batimer.app.test_client()
		response = app.post('/', 
			data={
				'date1' : '05/08/2014',
				'time1' : '09:00:00',
				'date2' : '05/08/2014',
				'time2' : '13:00:00',
			}
		)
		self.assertIn('2014-05-08', response.data)
		self.assertIn('09:00:00', response.data)
		self.assertIn('13:00:00', response.data)

	def test_batimer_convert_post_date_to_datetime(self):
		date = '05/08/2014'
		time = '14:40:02'
		converted_time = batimer.convert_to_datetime(date, time)
		self.assertEquals(datetime.datetime(2014, 5, 8, 14, 40, 2), converted_time)

	def test_batimer_convert_to_datetime_false_when_bad_post_date(self):
		date1 = '13/03/2014'
		time1 = '11:13:41'
		date2 = '05/08/2014'
		time2 = '52802'
		self.assertFalse(batimer.convert_to_datetime(date1, time1))
		self.assertFalse(batimer.convert_to_datetime(date2, time2))

	def test_batimer_can_ignore_bad_post_data(self):
		app = batimer.app.test_client()
		response = app.post('/', 
			data={
				'date1' : 'poop',
				'time1' : 'baddata',
				'date2' : 'whomp',
				'time2' : 'incorrect',
			}
		)
		self.assertEquals('Inputted times were incorrect!', response.data)
	
	def test_batimer_can_get_db_data(self):
		app = batimer.app.test_client()
		response = app.post('/', 
			data={
				'date1' : '05/08/2014',
				'time1' : '09:00:00',
				'date2' : '05/10/2014',
				'time2' : '13:00:00',
			}
		)
		self.assertIn('2014-05-08 20:55:28\t', response.data)

	def test_batimer_can_can_handle_empty_db_data(self):
		app = batimer.app.test_client()
		response = app.post('/', 
			data={
				'date1' : '05/08/2009',
				'time1' : '11:00:00', 
				'date2' : '05/10/2009',
				'time2' : '13:00:00', 
			}
		)
		self.assertIn('No data found in this range', response.data)

class BatimerModels(unittest.TestCase):
	def test_batimer_can_create_and_read_rows_in_model(self):
		current_time = datetime.datetime(2014, 5, 8, 20, 55, 28)
		row = Status(current_time, 2749.42)
		db.session.add(row)
		db.session.commit()
		statuses = Status.query.filter_by(id=row.id)
		self.assertEquals(current_time, statuses[0].recorded_time)

if __name__ == '__main__':
	unittest.main()
