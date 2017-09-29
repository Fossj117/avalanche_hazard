import requests 
import datetime
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "http://jhavalanche.org/viewTeton"

def create_dates(years = [2013, 2014,2015,2016], season_start = (9,1), season_length = 9*30): 
	''' Create a list of dates'''

	dates = []

	for year in years: 

		base = datetime.datetime(year, season_start[0], season_start[1])
		yr_dates = [base + datetime.timedelta(days = x) for x in range(0,season_length)]

		dates = dates + yr_dates

	return ['-'.join([str(i.year), str(i.month), str(i.day)]) for i in dates]

def get_data_row_from_request(r,date): 
	''' Convert the request results into data''' 

	soup = BeautifulSoup(r.content)

	try: 
		table = soup.findAll('table')[2]

		rows = [] 

		for row in table.findAll('tr'): 
			row = [val.text for val in row.find_all('td')] + [date]
			rows.append(row)

	except: 
		# No data
		empty = [0,0,0, date]
		rows = [empty, empty, empty]

	return rows

if __name__ == "__main__": 

	dates = create_dates()

	results = []

	for date in dates: 

		print "Got {}".format(date)

		r = requests.get(BASE_URL, params = {'data_date': date, 'template': 'teton_print.tpl.php'})
		rows = get_data_row_from_request(r,date)

		results = results + rows

	df = pd.DataFrame(results)
	df.columns = ['Elevation', 'Morning', 'Afternoon', 'Date']

	df.to_csv('avalanche_hazard.csv', encoding = 'utf-8')