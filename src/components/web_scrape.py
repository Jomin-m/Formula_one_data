import pandas as pd
import requests
from bs4 import BeautifulSoup
from src.logger import logging

def collect_race_data():
    # list to store all race data
    races = []

    # iterate through each year
    for year in range(1950, pd.Timestamp.now().year):
        print(f"Collecting data for year {year}")

        # get the list of rounds for the year
        r = requests.get(f"https://ergast.com/api/f1/{year}.json")
        json_data = r.json()
        rounds = json_data["MRData"]["RaceTable"]["Races"]

        # iterate through each round and collect race data
        for race in rounds:
            race_dict = {}
            race_dict["season"] = year
            race_dict["Round"] = race["round"]
            race_dict["circuit_id"] = race['Circuit']['circuitId']
            race_dict["lat"] = race['Circuit']['Location']['lat']
            race_dict["long"] = race['Circuit']['Location']['long']
            race_dict["country"] = race['Circuit']['Location']['country']
            race_dict["date"] = race['date']
            race_dict["url"] = race['url']
            races.append(race_dict)

    # create a pandas dataframe from the collected data
    race_data = pd.DataFrame(races)

    # save the dataframe to a CSV file
    race_data.to_csv("race_data.csv", index=False)

def collect_driver_standings():
    # list to store all driver standings data
    race_driverstandings = []

    # iterate through each year
    for year in range(1950, pd.Timestamp.now().year):
        print(f"Collecting data for year {year}")

        # get the list of rounds for the year
        r = requests.get(f"https://ergast.com/api/f1/{year}.json")
        json_data = r.json()
        rounds = json_data["MRData"]["RaceTable"]["Races"]

        # iterate through each round and collect driver standings data
        for round_data in rounds:
            url = f'https://ergast.com/api/f1/{year}/{round_data["round"]}/driverStandings.json'
            r = requests.get(url)
            json_data = r.json()
            driver_standings = json_data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

            # iterate through each driver in the standings and collect their data
            for driver in driver_standings:
                race_dict = {}
                race_dict["season"] = year
                race_dict["round"] = round_data["round"]
                race_dict["race"] = round_data["raceName"]
                race_dict["date"] = round_data["date"]
                race_dict["driver"] = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
                race_dict["points"] = driver['points']
                race_dict["wins"] = driver['wins']
                race_driverstandings.append(race_dict)

    # create a pandas dataframe from the collected data
    driver_standings_data = pd.DataFrame(race_driverstandings)

    # save the dataframe to a CSV file
    driver_standings_data.to_csv("driver_standings.csv", index=False)

def results_driver_standings():
    # list to store all driver standings data
    results_driverstandings = []

       # iterate over years and rounds
    for year in range(1950, pd.Timestamp.now().year):
        print(f"Collecting data for year {year}")
        r = requests.get(f"http://ergast.com/api/f1/{year}/results.json")
        json_data = r.json()

        # iterate over each race result
        for race_result in json_data["MRData"]["RaceTable"]["Races"]:
            for result in race_result["Results"]:
              
              race_dict = {}
              race_dict["season"] = race_result["season"]
              race_dict["round"] = race_result["round"]
              race_dict["circuit_id"] = race_result["Circuit"]["circuitId"]
              race_dict["driver"] = result["Driver"]["driverId"]
              race_dict["dob"] = result["Driver"]["dateOfBirth"]
              race_dict["nationality"] = result["Driver"]["nationality"]
              race_dict["constructor"] = result["Constructor"]["constructorId"]
              race_dict["grid"] = result["grid"]
              race_dict["time"] = race_result["Time"]["millis"]if 'Time' in race_result else None
              race_dict["status"] = result["status"]
              race_dict["points"] = result["points"]
              race_dict["podium"] = result["position"]

              results_driverstandings.append(race_dict)
    # create a pandas dataframe from the collected data
    results_f1 = pd.DataFrame(results_driverstandings)

    # save the dataframe to a CSV file
    results_f1.to_csv("results_driverstandings.csv", index=False)


def constructor_results_data():
    results_constructor_standings = []

    for year in range(1950, pd.Timestamp.now().year):
        print(f"Collecting data for year {year}")

        url = f"https://ergast.com/api/f1/{year}.json"
        r = requests.get(url)
        json_data = r.json()
        rounds = json_data["MRData"]["RaceTable"]["Races"]

        for rd in rounds:
            round_number = rd["round"]
            url = f"https://ergast.com/api/f1/{year}/{round_number}/ConstructorStandings.json"
            r = requests.get(url)
            json_data = r.json()
            standings_table = json_data["MRData"]["StandingsTable"]

            if 'StandingsLists' in standings_table and standings_table['StandingsLists']:
                for constructor in standings_table['StandingsLists'][0]['ConstructorStandings']:
                    race_dict = {}
                    race_dict["season"] = year
                    race_dict["round"] = round_number
                    race_dict["constructor"] = constructor['Constructor']['constructorId']
                    race_dict["constructor_points"] = constructor['points']
                    race_dict["constructor_wins"] = constructor['wins']
                    race_dict["constructor_standing_position"] = constructor['position']
                    results_constructor_standings.append(race_dict)

    constructor_standings_data = pd.DataFrame(results_constructor_standings)
    constructor_standings_data.to_csv("constructor_standings.csv", index=False)


def get_qualifying_results():
    qualifying_results = pd.DataFrame()

    for year in range(1950, pd.Timestamp.now().year):
        print(f"Collecting data for year {year}")

        url = f'https://www.formula1.com/en/results.html/{year}/races.html'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # find links to all circuits for a certain year
        year_links = []
        for page in soup.find_all('a', attrs={'class': "resultsarchive-filter-item-link FilterTrigger"}):
            link = page.get('href')
            if f'/en/results.html/{year}/races/' in link:
                year_links.append(link)

        # for each circuit, switch to the starting grid page and read table
        year_df = pd.DataFrame()
        new_url = 'https://www.formula1.com{}'
        for n, link in enumerate(year_links):
            link = link.replace('race-result.html', 'starting-grid.html')
            df = pd.read_html(new_url.format(link))
            df = df[0]
            df['season'] = year
            df['round'] = n + 1
            for col in df:
                if 'Unnamed' in col:
                    df.drop(col, axis=1, inplace=True)

            year_df = pd.concat([year_df, df])

        # concatenate all tables from all years
        qualifying_results = pd.concat([qualifying_results, year_df])

    # rename columns
    qualifying_results.rename(columns={'Pos': 'grid', 'Driver': 'driver_name', 'Car': 'car',
                                       'Time': 'qualifying_time'}, inplace=True)
    # drop driver number column
    qualifying_results.drop('No', axis=1, inplace=True)

   
    qualifying_results.to_csv("qualifying_results.csv", index=False)

def get_race_weather(races):
    weather = races.iloc[:,[0,1,2]]
    info = []

    for link in races.url:
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.text, 'html.parser')
            tables = soup.find_all('table')
            weather_found = False
            
            for table in tables:
                headers = table.find_all('th')
                for header in headers:
                    if header.text.strip().lower() == 'weather':
                        weather_row = header.parent
                        info.append(weather_row.find('td').text.strip())
                        weather_found = True
                        break
                if weather_found:
                    break
            
            if not weather_found:
                info.append('not found')
            
        except:
            info.append('not found')

    weather['weather'] = info

    weather_dict = {'weather_warm': ['soleggiato', 'clear', 'warm', 'hot', 'sunny', 'fine', 'mild', 'sereno'],
                    'weather_cold': ['cold', 'fresh', 'chilly', 'cool'],
                    'weather_dry': ['dry', 'asciutto'],
                    'weather_wet': ['showers', 'wet', 'rain', 'pioggia', 'damp', 'thunderstorms', 'rainy'],
                    'weather_cloudy': ['overcast', 'nuvoloso', 'clouds', 'cloudy', 'grey', 'coperto']}
    
    weather_df = pd.DataFrame(columns = weather_dict.keys())
    for col in weather_df:
        weather_df[col] = weather['weather'].map(lambda x: 1 if any(i in weather_dict[col] for i in x.lower().split()) else 0)

    weather_info = pd.concat([weather, weather_df], axis = 1)
    weather_info.to_csv("weather_info.csv", index=False)


if __name__ =="__main__":
    logging.info("Web Scraping in Progress-----")
    #race_data = collect_race_data()
    #driver_standings_data = collect_driver_standings()
    #results_f1 =results_driver_standings()
    #constructor_f1 =constructor_results_data()
    #get_qualifying_results()
    #race_data_input = pd.read_csv("race_data.csv")
    #get_race_weather(race_data_input)
    logging.info("Web Scraping is Completed")