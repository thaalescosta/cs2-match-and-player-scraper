from io import BytesIO
from PIL import Image, UnidentifiedImageError
import requests
import os
import time
import numpy as np
import pandas as pd

def download_photos(players_data):
    """
    Gets player photos and flags from HLTV and saves them locally.
    
    """
    
    headers = {
    "authority": "img-cdn.hltv.org",
    "method": "GET",
    "path": "/playerbodyshot/rl_4NtItqpjwLHZL12oMNb.png?ixlib=java-2.1.0&w=400&s=e017b74a48aab673759886475cdfac23",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "cookie": "cf_clearance=FV9QsL0R6xwDiTHCGsAJ..NTVDJCiFOzNt7c_SQevY8-1739468146-1.2.1.1-qBWa2RrtZ2csRcGN1qI8f2tf8Xdw8zFEVEAYBSErNskfS3sNvTZ.tBIwif.W6_9IS5VF39zbMVco7NALzmo2LGr0NfC733NpQf_Db7_5E813oDZCGd8R5QLziH8TgGqfzwxEKqEx_8VIk7YZ7Z7_BcSTW8ncRkfkd6ph26IaEbz42D_kYcHi1JTY2jnGuGjrEU5ha1F5F9CrlstCTyhs6smdSKbgsl6JsggRrg9dMFmjh7nQ.JF4yfMxhC22tNh85iE0w.dXcZ_F91u6VxpjaPNQk2ubhgz2z2S.UWChdUM7RfcZfZmLOVGVU9WBH1_O0_bUdPbKDM0Sz2IcKHPsWQ; __cf_bm=YtWAznoBgdWWvBivue5Gy58j2SDoqWJxKjGhAgqYyRw-1739474401-1.0.1.1-vwS3AXNGXgGivAPR0KrZCrzncJN03BjjQYblFWvkkk2MtH.7PzihwzbPKuE_KqLmXCcY67KR5yMHuqcqz7H1gg",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    headers2 = {
        "authority": "www.hltv.org",
        "method": "GET",
        "path": "/img/static/player/player_silhouette.png",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "cookie": "MatchFilter={%22active%22:false%2C%22live%22:false%2C%22stars%22:1%2C%22lan%22:false%2C%22teams%22:[]}; CookieConsent={stamp:%273NgGg27hj0ejKpNtm87m/YBPSLnL4lNd/yPbJihd+Z9o9RYqFbPN7w==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1733077873420%2Cregion:%27br%27}; statsTablePadding=medium; cf_clearance=P9ijKyCwD8a5rm1I4Boz3YOaqBR15KXAKcree6_8h44-1739476131-1.2.1.1-dpg52IEOA5ltYBkGfLlZQsRgsvPRGYR2AfHk6HJ4m8oAnluwip2cKjL0TN0kf5DaIx8OJv5iz7kaNBoeIts3twQY4_3KEs4XOSHUbZEZWrfA.EjF3OsZeygwVnfJK91sES_y8yPVYsJSP3uz1pgNscIBbG1RZv_UYX.BNabSdLIBlo4uEKe.X6Ch1jm0Im81oOHnlhjfA1MsVywssC_aW9KZJsIBrYi31zz5IVOBb.ujCz1KLpcNEu0Uh3EUKCRuFZO9IzO.ZakFdvmynC9Pi_ltW..OJQEJEvuRZCnuEXiv8oaKkfcR_ZlnO0ZIFE4uM51jyX31Jx4kguz2_vcqZg; __cf_bm=jMzLwRjGt4MV2hgtoWTP8HEeoqiqgocRBhKJuVeVruM-1739476402-1.0.1.1-eFHtIuMZGyiud7rxFO3OxN4WQkKV9Lr5E8NqGkXU4dOV4kqOcEm1i.sjYk9coOrbwvvA5DzlqiZaGUFa.rYffw",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
        "sec-ch-ua-arch": "\"x86\"",
        "sec-ch-ua-bitness": "\"64\"",
        "sec-ch-ua-full-version": "\"133.0.6943.99\"",
        "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"133.0.6943.99\", \"Chromium\";v=\"133.0.6943.99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua-platform-version": "\"10.0.0\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    headers3 = {
        "authority": "www.hltv.org",
        "method": "GET",
        "path": "/img/static/flags/30x20/UY.gif",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "cookie": "MatchFilter={%22active%22:false%2C%22live%22:false%2C%22stars%22:1%2C%22lan%22:false%2C%22teams%22:[]}; CookieConsent={stamp:%273NgGg27hj0ejKpNtm87m/YBPSLnL4lNd/yPbJihd+Z9o9RYqFbPN7w==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1733077873420%2Cregion:%27br%27}; statsTablePadding=medium; cf_clearance=eMwcm5Xn7zmbnk2m_JFct3sEd.h_Gb9s65S6FNsCsPA-1739493069-1.2.1.1-LuKuIO4cVAaJKiDutA5K0_4l14_6hmWFC6achrycrH.sX1n4lPyck5FA1nR16TqBbgbet.kq4Ik1jyVkgigL3LDJqS2dhQrXxTZl7muRwqiCJDn4H8ZajxIQPKAg3.VckGiyBlEhUIdzUv5xuGJkv_qx0EkOdOuq1RLjVqejb4B82L_LnaLOJ9wWu7Ow2k9p1XieyhmxRBerfg2PLBYUc7ztx_1hA9z3ZLMhBzpITvYxG8vmjFd6J5w4Y7wJFgRJXKF4rC2CzQOb1Rq2NW4g4oCJYyZVJHq1W8Yp9bhrU2fej7bzwOuKcSFVn01ptQyFbNr084YFFpTVBu.5Qlyk6Q; __cf_bm=Zei4mU4WT3we61ryZnV8pBU5TP4hnYNhzuGehlaP_KQ-1739494899-1.0.1.1-rL1JEND5HWPz7eZM_Z2KlzollyOKz3jpuqHHUpRrjri.MIDk1PwRXJgtbcT_8_7oTwHvP9P8f6anDKzJXrD01A",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
        "sec-ch-ua-arch": "\"x86\"",
        "sec-ch-ua-bitness": "\"64\"",
        "sec-ch-ua-full-version": "\"133.0.6943.99\"",
        "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"133.0.6943.99\", \"Chromium\";v=\"133.0.6943.99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-ua-platform-version": "\"10.0.0\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    output_dir = os.path.join("ExtractPlayerData", "photo_players")
    output_dir_flags = os.path.join("ExtractPlayerData", "photo_players", "_flags")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(output_dir_flags):
        os.makedirs(output_dir_flags)

    for index, row in players_data.iterrows():
        time.sleep(0.1)
        player_name = row['player_name']
        player_nick = row['player_nick']
        photo_player = row['photo_player']
        player_flag = row['player_flag']
        
        if "player_silhouette" in photo_player or photo_player == None:
            response = requests.get('https://www.hltv.org/img/static/player/player_silhouette.png', headers=headers2)
        else:
            response = requests.get(photo_player, headers=headers)
        
        try:
            img = Image.open(BytesIO(response.content))
            img.save(os.path.join(output_dir, f"{row['team_name'].lower().replace(' ', '-')}-{player_nick}.png"))
        except UnidentifiedImageError:
            print(f"Could not identify image for URL: {photo_player}")
            
        if pd.isna(row['player_flag']):
            continue
        else:
            response2 = requests.get(player_flag, headers=headers)
        
        try:
            img = Image.open(BytesIO(response2.content))
            img.save(os.path.join(output_dir_flags, f"{row['player_country'].lower().replace(' ','-')}.png"))
        except UnidentifiedImageError:
            print(f"Could not identify image for URL: {player_flag}")
        
        # Update the DataFrame with the local file paths
        players_data.loc[index, 'photo_player_path'] = os.path.abspath(os.path.join(output_dir, f"{row['team_name'].lower().replace(' ', '-')}-{player_nick}.png"))
        players_data.loc[index, 'player_flag_path'] = os.path.abspath(os.path.join(output_dir_flags, f"{row['player_country'].lower().replace(' ','-')}.png"))
    
    print(f"\nAll players who had their photos on HLTV have been downloaded")
    
    return players_data
