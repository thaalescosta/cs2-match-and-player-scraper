import os
import time
from _functions.chromelib import WebDriverWait, Service, Options, webdriver

def download_files(*download_links, camp, raiz):
    destination_folder = os.path.join(raiz, "Downloads", camp)
    print(f"\nDownloading .RAR files for each matchup")
    # Create the destination folder if it doesn't exist
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
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--silent')
    chrome_options.add_argument('--disable-logging')
    
    # Initialize the undetected Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # Function to wait for downloads to complete
    def wait_for_downloads_to_complete(download_folder, expected_files, timeout=300):
        """
        Wait for all expected files to be downloaded.
        :param download_folder: Path to the download folder.
        :param expected_files: List of expected filenames.
        :param timeout: Maximum time to wait (in seconds).
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Check if all expected files exist and are not partially downloaded
            downloaded_files = [f for f in os.listdir(download_folder) if not f.endswith(".crdownload")]
            if all(file in downloaded_files for file in expected_files):
                print("All files have been downloaded.")
                return
            time.sleep(1)
        print("Timeout reached. Some downloads may not have completed.")

    # Extract filenames from URLs
    expected_files = [url.split("/")[-1] for url in download_links]

    # Loop through each URL and download the file
    for url in download_links:
        nome = url.rsplit("-", 1)[0].rsplit("/", 1)[-1]
        try:
            driver.get(url)  # Open the URL in the browser
            time.sleep(1)  # Wait for the download to start (adjust as needed)
        except Exception as e:
            print(f"Download failed: {nome} (Erro: {e})")  # Print the error message if download fails

    # Wait for all downloads to complete
    wait_for_downloads_to_complete(destination_folder, expected_files)

    driver.quit()
