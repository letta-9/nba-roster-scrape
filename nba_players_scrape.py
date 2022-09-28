from bs4 import BeautifulSoup as Soup
import requests
import pandas as pd
from pandas import DataFrame


teams = ['Boston-Celtics/2', 'Brooklyn-Nets/38', 'New-York-Knicks/20', 'Philadelphia-Sixers/22', 'Toronto-Raptors/28', 'Chicago-Bulls/4', 'Cleveland-Cavaliers/5', 
            'Detroit-Pistons/8', 'Indiana-Pacers/11', 'Milwaukee-Bucks/16', 'Atlanta-Hawks/1', 'Charlotte-Hornets/3', 'Miami-Heat/15', 'Orlando-Magic/21', 'Washington-Wizards/30', 
                'Denver-Nuggets/7', 'Minnesota-Timberwolves/17', 'Oklahoma-City-Thunder/33', 'Portland-Trail-Blazers/24', 'Utah-Jazz/29', 'Golden-State-Warriors/9', 'Los-Angeles-Clippers/12', 
                    'Los-Angeles-Lakers/13', 'Phoenix-Suns/23', 'Sacramento-Kings/25', 'Dallas-Mavericks/6', 'Houston-Rockets/10', 'Memphis-Grizzlies/14', 'New-Orleans-Pelicans/19', 'San-Antonio-Spurs/26']

players = []
players_df = pd.DataFrame(players)

for x in teams:

    response = requests.get(f'https://basketball.realgm.com/nba/teams/{x}/Rosters/Regular/2023')
    soup = Soup(response.text, 'lxml')
    tables = soup.find_all('table')

    data = tables[0]
    rows = data.find_all('tr')

    def parse_row(row):
        return [str(x.string) for x in row.find_all('a')]

    list_of_parsed_rows = [parse_row(row) for row in rows]
    data_df = DataFrame(list_of_parsed_rows)

    players_df = pd.concat([players_df, data_df])



players_df.rename(columns = {0:'name'}, inplace=True)
players_df = players_df['name'].str.lower()
players_df = players_df.str.replace('[^\w\s]','')
players_df = players_df.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
players_df = players_df.dropna()

players_df.to_csv('nba_list.csv', index=False)
