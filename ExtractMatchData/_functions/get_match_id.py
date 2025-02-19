import time
import threading
from ExtractMatchData._functions.chromelib import By, WebDriverWait, EC, get_chrome_options
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_match_ids(tournaments_df):
    total_matches = len(tournaments_df['url'])
    
    # Create tqdm progress bar
    pbar = tqdm(
        total=total_matches,
        desc="Fetching Match IDs ",
        unit="match",
        ncols=100,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
    )

    # Function to refresh tqdm every second
    def refresh_tqdm():
        while not pbar.n >= total_matches:
            pbar.refresh()
            time.sleep(1)  # Refresh every second

    # Start refresh thread
    refresh_thread = threading.Thread(target=refresh_tqdm, daemon=True)
    refresh_thread.start()
    
    for i, match in enumerate(tournaments_df['url'], 1):
        time.sleep(0.2)
        driver = get_chrome_options()
        driver.get(match)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        team1_div = soup.find('div', class_='team1-gradient')
        if team1_div:
            team1_name = team1_div.find('div', class_='teamName').text
            score_div = team1_div.find('div', class_=['won', 'lost'])
            team1_score = score_div.text if score_div else None
            
        team2_div = soup.find('div', class_='team2-gradient')
        if team2_div:
            team2_name = team2_div.find('div', class_='teamName').text
            score_div = team2_div.find('div', class_=['won', 'lost'])
            team2_score = score_div.text if score_div else None
        
        # Get match format (Bo1, Bo3, Bo5)
        format_div = soup.find('div', class_='padding preformatted-text')
        if format_div:
            format_text = format_div.text.strip()
            if "Best of 5" in format_text:
                match_format = "Bo5"
            elif "Best of 3" in format_text:
                match_format = "Bo3" 
            elif "Best of 1" in format_text:
                match_format = "Bo1"
            else:
                match_format = None
        else:
            match_format = None
        
        # Get match date
        date_div = soup.find('div', class_='date')
        if date_div and 'data-unix' in date_div.attrs:
            unix_timestamp = int(date_div['data-unix']) / 1000  # Convert milliseconds to seconds
            match_date = time.strftime('%Y-%m-%d', time.localtime(unix_timestamp))
        else:
            match_date = None     
        
        try:
            cookie_accept_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            cookie_accept_button.click()
        except Exception as e:
            print("Cookies notification not found:", e)

        time.sleep(0.3)

        results_holder = soup.find('div', class_='vod-text-box')
        if results_holder:
            for id_tag in results_holder.find_all('a', href=True):
                href = id_tag['href']
                match_id = href.split("/")[-1]
        tournaments_df.at[i-1, 'match_id'] = match_id
        tournaments_df.at[i-1, 'match_format'] = match_format
        tournaments_df.at[i-1, 'match_date'] = match_date
        tournaments_df.at[i-1, 'team_1'] = team1_name
        tournaments_df.at[i-1, 'team_1_result'] = team1_score
        tournaments_df.at[i-1, 'team_2'] = team2_name
        tournaments_df.at[i-1, 'team_2_result'] = team2_score


        driver.quit()
        time.sleep(0.2)

        # Update progress bar
        pbar.update(1)

    pbar.close()
    return tournaments_df