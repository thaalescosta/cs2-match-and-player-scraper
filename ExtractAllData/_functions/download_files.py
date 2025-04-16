import os
import time
from tqdm import tqdm  # Import tqdm for the progress bar
from ExtractAllData._functions.chromelib import Options, webdriver
import shutil

def download_files(tournaments_df):
        
    destination_folder = os.path.join(tournaments_df.iloc[0]['root'], "downloads", 'demos')
    os.makedirs(destination_folder, exist_ok=True)
        
    prefs = {
        "download.default_directory": destination_folder,  # Set the download directory
        "download.prompt_for_download": False,  # Disable download prompts
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    chrome_options = Options()        
    chrome_options.add_argument('--headless=new')
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/13.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--silent')
    chrome_options.add_argument('--disable-logging')
    
    # Initialize the Chrome driver with longer timeout
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(300)  # Set page load timeout to 5 minutes

    # Get unique download links
    unique_download_links = tournaments_df['direct_url_demo'].unique()
    expected_files = [url.split("/")[-1] for url in unique_download_links]
    
    # Initialize tqdm progress bar
    progress_bar = tqdm(total=len(expected_files),
                        desc="Downloading .rar   ", 
                        maxinterval=1.0,
                        unit="file",
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
                        ncols=100,  # Adjust the width of the progress bar
                        )

    # Function to monitor the download progress
    def update_progress_bar():
        """Updates the progress bar based on downloaded .rar files"""
        while progress_bar.n < len(expected_files):
            downloaded_files = [f for f in os.listdir(destination_folder) if f.endswith(".rar")]
            progress_bar.n = len(downloaded_files)
            progress_bar.refresh()
            time.sleep(1)  # Check every second
    
    # Start tracking downloads in a separate thread
    from threading import Thread
    progress_thread = Thread(target=update_progress_bar, daemon=True)
    progress_thread.start()
    
    # Loop through each unique URL and download the file
    for url in unique_download_links:
        nome = url.rsplit("-", 1)[0].rsplit("/", 1)[-1]
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                driver.get(url)  # Open the URL in the browser
                time.sleep(2)  # Increased wait time between downloads
                break  # If successful, break the retry loop
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    print(f"Download failed after {max_retries} attempts: {nome} (Error: {e})")
                else:
                    print(f"Attempt {retry_count} failed, retrying download for {nome}...")
                    time.sleep(5)  # Wait before retrying

    # Wait for all expected files to be downloaded
    while len([f for f in os.listdir(destination_folder) if f.endswith(".rar")]) < len(expected_files):
        time.sleep(1)  # Check every second

    progress_bar.n = len(expected_files)  # Ensure progress bar reaches 100%
    progress_bar.refresh()
    progress_bar.close()
    driver.quit()
    
    # Create a standardized filename for each demo file using event_id and match_id
    # Format: E{event_id}_M{match_id}_{original_filename}
    tournaments_df['file_name'] = tournaments_df.apply(
        lambda row: f"E{row['event_id']}_M{row['match_id']}_{row['direct_url_demo'].split('/')[-1]}", 
        axis=1
    )
    
    # Rename downloaded files to add the prefix
    for _, row in tournaments_df.iterrows():
        old_name = row['direct_url_demo'].split('/')[-1]
        new_name = f"E{row['event_id']}_M{row['match_id']}_{old_name}"
        old_path = os.path.join(destination_folder, old_name)
        new_path = os.path.join(destination_folder, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)

    return tournaments_df