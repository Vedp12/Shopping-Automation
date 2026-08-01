import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

url = "https://www.football-data.co.uk/englandm.php"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers, timeout=10)
soap = bs(response.text, "html.parser")
all_anchor = soap.find_all("a", href=True)

for anchor in all_anchor:
    if anchor["href"].lower().endswith(".csv"):
        csv_url = urljoin(url, anchor["href"])

        csv_Data = pd.read_csv(csv_url)
        print(csv_url)
        # a = pd.read_csv(andhor[.c])
# tables = pd.read_csv(url)

# a = pd.read_csv('https://www.football-data.co.uk/mmz4281/2526/E0.csv')
# a.rename(columns={'FTHG':'Home_goals','FTAG':'away_goals'},inplace=True)
# print(a)
