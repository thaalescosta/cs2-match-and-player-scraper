import time
from _functions.chromelib import By, WebDriverWait, EC, get_chrome_options
from bs4 import BeautifulSoup
import replit


def get_urls(event_id):
    replit.clear()
    
    driver = get_chrome_options()

    url = f"https://www.hltv.org/results?event={event_id}"
    driver.get(url)

    try:
        cookie_accept_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        cookie_accept_button.click()
    except Exception as e:
        print("Cookies notification not found:", e)

    # Wait for the page to load
    time.sleep(1)

    # Retrieve the HTML content of the page and tournament name
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    results_holder = soup.find('div', class_='results-holder')
    if not results_holder:
        print("No results found for the given event.")
        driver.quit()
        return [], camp_name, camp_var
    camp_name = soup.find('div', class_='event-hub-title').text.strip()
    camp_var = soup.find('a', class_='event-hub-top')['href'].split('/')[-1]
    
    print(f"Event: {camp_name}\n")
    
    # Fetch the URLs of all HLTV match pages for the event
    match_urls = []
    i=1
    for a_tag in results_holder.find_all('a', href=True):
        href = a_tag['href']
        full_url = f"https://www.hltv.org{href}"
        match_urls.append(full_url)

    print(f"Number of Matchups: {len(match_urls)}")
    print()

    driver.quit()
    
    return match_urls, camp_name, camp_var