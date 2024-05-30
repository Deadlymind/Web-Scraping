import requests
from bs4 import BeautifulSoup
import csv


date = input("Enter Date (format: MM/DD/YYYY): ")
page = requests.get(f"https://www.yallakora.com/match-center/مركز-المباريات?date={date}")

def main(page):

    source = page.content
    soup = BeautifulSoup(source, 'lxml')
    matches_details = []

    # championship = soup.find_all('div', class_="")
    championship = soup.find_all('div', {'class': 'matchCard'})
    print(championship)




main(page)