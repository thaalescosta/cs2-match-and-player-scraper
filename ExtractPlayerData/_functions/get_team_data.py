from ExtractMatchData._functions.chromelib import get_chrome_options, By, WebDriverWait, EC, pd
from bs4 import BeautifulSoup

def get_team_data(url, topN=40):
    driver = get_chrome_options()
    driver.get(url)

    try:
        cookie_accept_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        cookie_accept_button.click()
    except Exception as e:
        print("Cookies notification not found:", e)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ranked-team"))
    )

    # Retrieve the HTML content of the page
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the first topN ranked teams
    teams = soup.find_all('div', class_='ranked-team standard-box', limit=topN)

    team_data = []

    for team in teams:
        team_name = team.find('span', class_='name').text
        team_page = f"https://www.hltv.org{team.find('a', class_='moreLink')['href'].replace(' ', '')}"
        allPlayers = team.find_all('td', class_='player-holder')
        
        if(len(allPlayers) == 4):
            team_data.append({
                'team_name': team_name,
                'team_page': team_page,
                'player_name': "missing_player",
                'player_country': "n/a", 
                'player_nick': "missing_player",
                'player_hltv_url': "no url"
            })
        
        for player in allPlayers:
            player_name = player.find('img', class_='playerPicture')['title']
            player_country = player.find('img', class_='gtSmartphone-only flag')['alt']
            player_nick = player.find('div', class_='nick').text.strip()
            player_hltv_url = player.find('a', class_='pointer')['href']

            team_data.append({
                'team_name': team_name,
                'team_page': team_page,
                'player_name': player_name,
                'player_country': player_country,
                'player_nick': player_nick,
                'player_hltv_url': f'https://www.hltv.org{player_hltv_url}'
            })

    driver.quit()

    # Create a pandas DataFrame from the team_data list
    return pd.DataFrame(team_data)