from ExtractMatchData._functions.chromelib import By, WebDriverWait, EC, get_chrome_options, pd
from bs4 import BeautifulSoup
import os
import time

def get_matches_url(*id_event, root):
    
    # Initialize an empty DataFrame with required columns
    tournaments_df = pd.DataFrame(columns=["root", "url", "url_event", "tournament", "nspc_tournament"])
    print("---------------------------------------------")
    print("       MATCHUPS CAN BE Bo1, Bo3 or Bo5")
    print("---------------------------------------------")
    for id in id_event:
        driver = get_chrome_options()
        url = f"https://www.hltv.org/results?event={id}"
        driver.get(url)

        try:
            cookie_accept_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            cookie_accept_button.click()
        except Exception as e:
            print("Cookies notification not found:", e)

        time.sleep(1)  # Wait for the page to load

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        results_holder = soup.find('div', class_='results-holder')

        if not results_holder:
            print("No results found for the given event.")
            driver.quit()
            continue  # Skip this event and proceed to the next one
        
        name = soup.find('div', class_='event-hub-title').text.strip()
        match_urls = [f"https://www.hltv.org{a['href']}" for a in results_holder.find_all('a', href=True)]

        # Append new rows to the DataFrame directly
        new_data = pd.DataFrame({
            "root": root,
            "url": match_urls,
            "url_event": url,
            "tournament": name,
            "nspc_tournament": name.lower().replace(' ', '-')
        })
        print(f'\nEvent: {new_data['tournament'].iloc[0]}\nNumber of matchups: {len(new_data)}')
        tournaments_df = pd.concat([tournaments_df, new_data], ignore_index=True)

    driver.quit()
    print(f"\n\nTotal number of matchups: {len(tournaments_df)}\n---------------------------------------------")
    
    return tournaments_df
