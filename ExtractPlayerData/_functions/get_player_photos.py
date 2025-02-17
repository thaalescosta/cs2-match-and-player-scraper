from ExtractPlayerData._functions.chromelib import get_chrome_options, WebDriverWait, EC, By, BeautifulSoup
import pandas as pd

def get_player_photos(players_data):
    """
    Fetches player photo URLs from HLTV team pages and adds them to the dataframe.
    
    """
    from tqdm import tqdm
    
    # Ensure the photo_player column exists
    if 'photo_player' not in players_data.columns:
        players_data['photo_player'] = None
        
    unique_team_pages = players_data['team_page'].unique()
    total_players = len(players_data)

    # Initialize the progress bar for total number of players
    progress_bar = tqdm(total=total_players,
                        desc="Fetching player photo URLs",
                        maxinterval=1.0,
                        unit="player",
                        ncols=100,
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
    )
    players_processed = 0

    for team_page in unique_team_pages:
        
        driver = get_chrome_options()
        
        driver.get(team_page)
        
        try:
            cookie_accept_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            cookie_accept_button.click()
        except Exception as e:
            print("Cookies notification not found:", e)
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bodyshot-team-bg"))
        )
        
        # Retrieve the HTML content of the page
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        
        team_name = soup.find('img', class_='team-logo')['alt']
        # Find the player pictures within the team page
        bodyshot_divs = soup.find_all('a', class_='col-custom', limit=5)    
        if len(bodyshot_divs) == 4:
            bodyshot_divs.append(None)
        
        for div in bodyshot_divs:
            if div is None or div.find('img', class_='bodyshot-team-img') is None:
                photo_player = "https://www.hltv.org/img/static/player/player_silhouette.png"
                player_nick = "missing_player"
                player_name = "missing_player"
                player_flag = None
                
            else:
                img_element = div.find('img', class_='bodyshot-team-img')
                photo_player = img_element['src']
                player_name = img_element['title']
                player_nick = img_element['title'].split("'")[1]
                flag_element = div.find('img', class_='flag')
                player_flag = f"https://www.hltv.org{flag_element['src']}" if flag_element else None
            
            matching_rows_url = players_data[(players_data['player_nick'] == player_nick) & (players_data['team_name'] == team_name)]
            
            # Update the DataFrame with the new player photo URL
            mask = (players_data['player_nick'].str.strip() == player_nick.strip()) & (players_data['team_name'].str.strip() == team_name.strip())
            players_data.loc[mask, 'photo_player'] = photo_player
            if player_flag:
                players_data.loc[mask, 'player_flag'] = player_flag
            # print(f'{player_nameplayer_countryplayer_flagplayer_countryphoto_player}')
            # Update progress for each player processed
            players_processed += len(matching_rows_url)
            progress_bar.update(len(matching_rows_url))

        driver.quit()

    # Close the progress bar
    progress_bar.close()

    players_data.loc[players_data['photo_player'].isna(), 'player_name'] = ("Player was Benched")
    players_data.loc[players_data['photo_player'].isna(), 'player_nick'] = "Benched"
    players_data.loc[players_data['photo_player'].isna(), 'photo_player'] = "https://www.hltv.org/img/static/player/player_silhouette.png"
    
    benched_count = len(players_data[players_data['photo_player'] == "https://www.hltv.org/img/static/player/player_silhouette.png"])
    
    if benched_count == 0:
        print(f"\nAll players had their photos downloaded")
    else:
        print(f"\nA total of {benched_count} players didn't have photos")


    players_data.to_csv('photo_players.csv',encoding='utf-8-sig', index=False)
    players_data.dropna(subset=['player_flag'], inplace=True)
    
    return players_data
