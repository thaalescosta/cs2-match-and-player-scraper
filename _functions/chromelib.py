#
# Just a simple function to get the chrome options for the selenium webdriver.
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os



def get_chrome_options():
    
    root = os.getcwd()
    
    chrome_options = Options()        
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--silent')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--no-sandbox')

    # Create service object with log output suppressed (getting rid of that DevTools is listening ...)
    service = Service(os.path.join(root, r"_resources","chromedriver.exe"))
    service.creation_flags = 0x08000000  # Suppress console window

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
