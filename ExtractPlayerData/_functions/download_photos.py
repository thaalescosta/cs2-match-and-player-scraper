from io import BytesIO
from PIL import Image, UnidentifiedImageError
import requests
import os
import time
import numpy as np
import pandas as pd
import cloudscraper

def download_photos(players_data):
    """
    Gets player photos and flags from HLTV and saves them locally.
    
    """
    scraper = cloudscraper.create_scraper()
    
    output_dir = os.path.join("ExtractPlayerData", "photo_players")
    output_dir_flags = os.path.join("ExtractPlayerData", "photo_players", "_flags")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(output_dir_flags):
        os.makedirs(output_dir_flags)

    for index, row in players_data.iterrows():
        time.sleep(1)
        
        player_nick = row['player_nick']
        photo_player = row['photo_player']
        player_flag = row['player_flag']
        
        if "player_silhouette" in photo_player or photo_player == None:
            response = scraper.get('https://www.hltv.org/img/static/player/player_silhouette.png') #, headers=headers2
        else:
            response = scraper.get(photo_player) #, headers=headers
        
        try:
            img = Image.open(BytesIO(response.content))
            img.save(os.path.join(output_dir, f"{row['team_name'].lower().replace(' ', '-')}-{player_nick}.png"))
        except UnidentifiedImageError:
            print(f"Could not identify image for URL: {photo_player}")
            
        if pd.isna(row['player_flag']):
            continue
        else:
            response2 = scraper.get(player_flag) #, headers=headers
        
        try:
            img = Image.open(BytesIO(response2.content))
            img.save(os.path.join(output_dir_flags, f"{row['player_country'].lower().replace(' ','-')}.png"))
        except UnidentifiedImageError:
            print(f"Could not identify image for URL: {player_flag}")
        
        # Update the DataFrame with the local file paths
        players_data.loc[index, 'photo_player_path'] = os.path.abspath(os.path.join(output_dir, f"{row['team_name'].lower().replace(' ', '-')}-{player_nick}.png"))
        players_data.loc[index, 'player_flag_path'] = os.path.abspath(os.path.join(output_dir_flags, f"{row['player_country'].lower().replace(' ','-')}.png"))
    
    print(f"\nThe progress bar not reaching 100% just means that some players don't have their photo on HLTV")
    
    return players_data
