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
        driver = get_chrome_options()
        driver.get(match)

        try:
            cookie_accept_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            cookie_accept_button.click()
        except Exception as e:
            print("Cookies notification not found:", e)

        time.sleep(0.3)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        results_holder = soup.find('div', class_='vod-text-box')
        if results_holder:
            for id_tag in results_holder.find_all('a', href=True):
                href = id_tag['href']
                match_id = href.split("/")[-1]
                tournaments_df.at[i-1, 'match_id'] = match_id

        driver.quit()
        time.sleep(0.2)

        # Update progress bar
        pbar.update(1)

    pbar.close()
    return tournaments_df