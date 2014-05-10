from flask import Flask, request, make_response, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://batimeruser:qwer1234@localhost/batimer'
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def main_page():
	if request.method == 'POST':
		output_data = ''
		time_start = convert_to_datetime(request.form['date1'], request.form['time1'])
		time_end = convert_to_datetime(request.form['date2'], request.form['time2'])
		if time_start and time_end:
			# read_time converts datetime objects to something more human readable
			read_time = lambda x : x.strftime('%Y-%m-%d %H:%M:%S') 
			output_data += 'Opto 22 data between the times starting from ' + \
				read_time(time_start) + ' to ' + read_time(time_end) + '\r\n'
			db_query = Status.query. \
				filter(Status.recorded_time > time_start). \
				filter(Status.recorded_time < time_end).all()
			if db_query != []:
				for status_row in db_query:
					output_data += read_time(status_row.recorded_time) + ',' + \
						str(status_row.torr) + '\r\n'
			else:
				output_data += ' | No data found in this range'
				response = make_response(output_data)
				return response
			response = make_response(output_data)
			data_filename = 'Opto22 Data ' + \
				read_time(time_start) + ' to ' + read_time(time_end)
			# filename cannot have spaces
			data_filename = data_filename.replace(' ', '-')
			# Change content disposition so we get a file
			response.headers['Content-Disposition'] = \
				'attachment; filename=' + data_filename + '.csv'
			return response
		else:
			return 'Inputted times were incorrect!'
	else:
		return render_template('main_page.html')

def convert_to_datetime(set_date, set_time):
	try:
		date = datetime.datetime.strptime(set_date, '%m/%d/%Y')
	except:
		return False
	# Get current date at midnight
	midnight = datetime.datetime.combine(date, datetime.time())
	try:
		time = datetime.datetime.strptime(set_time, '%H:%M:%S')
	except:
		return False
	# Convert current time to seconds from midnight
	seconds_int = (time - datetime.datetime(1900, 1, 1)).total_seconds()
	seconds_delta = datetime.timedelta( seconds=seconds_int )

	converted_time = midnight + seconds_delta
	return converted_time


class Status(db.Model):
	__tablename__ = 'Status'
	id = db.Column(db.Integer, primary_key=True)
	recorded_time = db.Column(db.DateTime)
	torr = db.Column(db.Float)

	def __init__(self, recorded_time, torr):
		self.recorded_time = recorded_time
		self.torr = torr
		pass

if __name__ == '__main__':
    app.run()
