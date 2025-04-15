import time
import threading
import pandas as pd
from ExtractAllData._functions.chromelib import By, WebDriverWait, EC, get_chrome_options
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

def process_match(row: pd.Series) -> List[Dict]:
    """Process a single match and return its data"""
    driver = get_chrome_options()
    try:
        driver.get(row['url'])
        time.sleep(0.5)  # Reduced wait time

        try:
            cookie_accept_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            cookie_accept_button.click()
        except:
            pass

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract match data
        match_data = extract_match_data(soup, row)
        return match_data
    finally:
        driver.quit()

def extract_match_data(soup: BeautifulSoup, row: pd.Series) -> List[Dict]:
    """Extract all match data from the soup object"""
    # Extract team data
    team1_div = soup.find('div', class_='team1-gradient')
    team2_div = soup.find('div', class_='team2-gradient')

    team1_name = team1_div.find('div', class_='teamName').text.strip() if team1_div else None
    team2_name = team2_div.find('div', class_='teamName').text.strip() if team2_div else None

    team1_score = team1_div.find('div', class_=['won', 'lost']).text.strip() if team1_div else None
    team2_score = team2_div.find('div', class_=['won', 'lost']).text.strip() if team2_div else None

    # Extract match format
    format_div = soup.find('div', class_='padding preformatted-text')
    format_text = format_div.text.strip() if format_div else ""
    match_format = get_match_format(format_text)

    # Extract match date
    match_datetime = extract_match_date(soup)

    # Extract match ID
    match_id = extract_match_id(soup)

    # Create base data
    base_data = {
        **row.to_dict(),
        'match_id': match_id,
        'match_format': match_format,
        'match_date': match_datetime,
        'team_1': team1_name,
        'team_1_result': team1_score,
        'team_2': team2_name,
        'team_2_result': team2_score,
        'winner': team1_name if team1_score and team2_score and int(team1_score) > int(team2_score) else team2_name,
        'event_id': row['url_event'].replace('https://www.hltv.org/results?event=', '')
    }

    # Extract map data
    return extract_map_data(soup, base_data)

def get_match_format(format_text: str) -> Optional[str]:
    """Extract match format from text"""
    if "Best of 5" in format_text:
        return "Bo5"
    elif "Best of 3" in format_text:
        return "Bo3"
    elif "Best of 1" in format_text:
        return "Bo1"
    return None

def extract_match_date(soup: BeautifulSoup) -> Optional[datetime]:
    """Extract match date from soup"""
    date_div = soup.find('div', class_='date')
    if date_div and 'data-unix' in date_div.attrs:
        unix_timestamp = int(date_div['data-unix']) / 1000
        return datetime.fromtimestamp(unix_timestamp)
    return None

def extract_match_id(soup: BeautifulSoup) -> Optional[str]:
    """Extract match ID from soup"""
    results_holder = soup.find('div', class_='vod-text-box')
    if results_holder:
        for id_tag in results_holder.find_all('a', href=True):
            href = id_tag['href']
            return href.split("/")[-1]
    return None

def extract_map_data(soup: BeautifulSoup, base_data: Dict) -> List[Dict]:
    """Extract map data from soup"""
    played_sections = soup.find_all('div', class_='played')
    if not played_sections:
        return [{**base_data, 'map': None, 'map_n': None}]

    map_data = []
    for section in played_sections:
        map_tag = section.find('div', class_='mapname')
        if map_tag:
            map_name = map_tag.text.strip()
            map_n = get_map_number(section)
            
            map_data.append({
                **base_data,
                'map': map_name,
                'map_n': map_n
            })
    
    return map_data

def get_map_number(section) -> Optional[str]:
    """Get map number from section"""
    parent_column = section.find_parent('div', class_='flexbox-column')
    if parent_column:
        mapholders = parent_column.find_all('div', class_='mapholder')
        for idx, mapholder in enumerate(mapholders, start=1):
            if section in mapholder.descendants:
                return f"m{idx}"
    return None

def get_match_ids(tournaments_df: pd.DataFrame) -> pd.DataFrame:
    """Main function to get match IDs using parallel processing"""
    all_matches_data = []
    total_matches = len(tournaments_df['url'])
    
    with tqdm(total=total_matches, desc="Fetching Match IDs", unit="match", ncols=100) as pbar:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_match, row) for _, row in tournaments_df.iterrows()]
            
            for future in as_completed(futures):
                match_data = future.result()
                all_matches_data.extend(match_data)
                pbar.update(1)

    # Map map names to CS2 standard
    map_name_mapping = {
        'Dust2': 'dust2',
        'Nuke': 'nuke',
        'Mirage': 'mirage',
        'Inferno': 'inferno',
        'Overpass': 'overpass',
        'Ancient': 'ancient',
        'Anubis': 'anubis',
        'Vertigo': 'vertigo',
        'Train': 'train',
        'Cache': 'cache',
    }

    df = pd.DataFrame(all_matches_data)
    df['map'] = df['map'].map(map_name_mapping).fillna(df['map'])
    return df