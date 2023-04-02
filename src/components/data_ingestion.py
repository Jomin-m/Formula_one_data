import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def ergast_api(table):
    current_year = datetime.now().year
    base_url = 'http://ergast.com/api/f1'
    years = range(1950, current_year+1)
    for year in years:
        response = requests.get(f'{base_url}/{year}/{table}.xml')
        soup = BeautifulSoup(response.content, 'lxml', features='xml')
        data = []
        if table == 'races':
            for race in soup.find_all('race'):
                row = {}
                row['season'] = race['season']
                row['round'] = race['round']
                row['date'] = race.date.text
                data.append(row)
            csv_file = f'{table}_{year}.csv'
        elif table == 'drivers':
            for driver in soup.find_all('driver'):
                row = {}
                row['driver_id'] = driver['driverId']
                row['code'] = driver.code.text if driver.code else ''
                row['dob'] = driver.dateOfBirth.text if driver.dateOfBirth else ''
                row['nationality'] = driver.nationality.text if driver.nationality else ''
                data.append(row)
            csv_file = f'{table}_{year}.csv'
        elif table == 'constructors':
            for constructor in soup.find_all('constructor'):
                row = {}
                row['constructor_id'] = constructor['constructorId']
                row['name'] = constructor.name.text
                row['nationality'] = constructor.nationality.text
                data.append(row)
            csv_file = f'{table}_{year}.csv'
        else:
            print('Invalid table name')
            return None
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f'{csv_file} saved successfully')


