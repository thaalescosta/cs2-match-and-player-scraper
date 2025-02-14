import time
from _functions.chromelib import By, WebDriverWait, EC, get_chrome_options
from bs4 import BeautifulSoup
from tqdm import tqdm  # Import tqdm for progress bar

def get_match_ids(*match_urls):
    match_ids = []

    # Iterate over all match URLs with a progress bar
    for match in tqdm(match_urls, desc="Fetching Match IDs", unit="match"):
        
        driver = get_chrome_options()
        driver.get(match)

        try:
            cookie_accept_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            cookie_accept_button.click()
        except Exception as e:
            print("Cookies notification not found:", e)

        time.sleep(1)

        # Retrieve the HTML content of the page
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Fetch the match ID to be used in the API request
        results_holder = soup.find('div', class_='vod-text-box')
        for id in results_holder.find_all('a', href=True):
            href = id['href']
            match_ids.append(href.split("/")[-1])
            
        driver.quit()
        
        time.sleep(0.2)

    return match_ids