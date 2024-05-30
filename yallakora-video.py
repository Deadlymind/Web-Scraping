import requests
from bs4 import BeautifulSoup
import csv

date = input("Enter Date (format: MM/DD/YYYY): ")
page = requests.get(f"https://www.yallakora.com/match-center/مركز-المباريات?date={date}")

def main(page):
    source = page.content
    soup = BeautifulSoup(source, 'lxml')
    matches_details = []

    championships = soup.find_all('div', {'class': 'matchCard'})

    def get_match_info(championship):
        championship_title_element = championship.contents[1].find('h2')
        championship_title = championship_title_element.text.strip() if championship_title_element else 'N/A'

        all_matches = championship.contents[3].find_all('div')
        number_of_matches = len(all_matches)

        for i in range(number_of_matches):
            # get team names
            team_A_element = all_matches[i].find('div', {'class': 'teamA'})
            team_B_element = all_matches[i].find('div', {'class': 'teamB'})
            team_A = team_A_element.text.strip() if team_A_element else 'N/A'
            team_B = team_B_element.text.strip() if team_B_element else 'N/A'

            # get score
            match_result_element = all_matches[i].find('div', {'class': 'MResult'})
            if match_result_element:
                match_result = match_result_element.find_all('span', {'class': 'score'})
                if match_result and len(match_result) >= 2:
                    score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
                else:
                    score = 'N/A'
            else:
                score = 'N/A'

            # get match time
            match_time_element = match_result_element.find('span', {'class': 'time'}) if match_result_element else None
            match_time = match_time_element.text.strip() if match_time_element else 'N/A'

            # add match info to matches_details
            matches_details.append({
                'championship_title': championship_title,
                'team_1': team_A,
                'team_2': team_B,
                'score': score,
                'match_time': match_time
            })

    for championship in championships:
        get_match_info(championship)

    # writing the match details to a csv file
    if matches_details:
        keys = matches_details[0].keys()
        with open('yallakora.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(matches_details)
            print('Done!')

main(page)
