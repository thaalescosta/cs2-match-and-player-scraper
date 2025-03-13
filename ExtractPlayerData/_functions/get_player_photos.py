from ExtractPlayerData._functions.chromelib import get_chrome_options, WebDriverWait, EC, By, BeautifulSoup

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
                        mininterval=0.5, # Set minimum update interval to 1 second
                        maxinterval=0.5,
                        unit="player",
                        ncols=100,
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
    )
    
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
        
        team_name = soup.find('h1', class_='profile-team-name text-ellipsis').text.strip()
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
            progress_bar.update(len(matching_rows_url))

           # Update the DataFrame with the new player photo URL
            mask = (players_data['player_nick'].str.strip() == player_nick.strip()) & (players_data['team_name'].str.strip() == team_name.strip())
            players_data.loc[mask, 'photo_player'] = photo_player
            if player_flag:
                players_data.loc[mask, 'player_flag'] = player_flag
               
        
        driver.quit()

    players_data.loc[players_data['photo_player'].isna(), 'player_name'] = ("Player was Benched")
    players_data.loc[players_data['photo_player'].isna(), 'player_nick'] = "Benched"
    players_data.loc[players_data['photo_player'].isna(), 'photo_player'] = "https://www.hltv.org/img/static/player/player_silhouette.png"
    players_data.loc[players_data['photo_player'].isna(), 'player_flag'] = "?"
    
    # Close the progress bar
    progress_bar.close()

    return players_data
