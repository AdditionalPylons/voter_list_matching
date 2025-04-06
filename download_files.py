import os
from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up download folder
cwd = os.getcwd()
download_folder = os.path.join(cwd, 'data')

# Configure Chrome options for automatic downloading
chrome_options = Options()
prefs = {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Start the driver
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://dl.ncsbe.gov/?prefix=Legal/Nov%202024%20Protests/Griffin/')

sleep(2)

# Find all links
links = driver.find_elements(By.CSS_SELECTOR, 'div#listing pre a')


# Set a headers dictionary to pretend like a normal browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                  "AppleWebKit/537.36 (KHTML, like Gecko) " \
                  "Chrome/122.0.0.0 Safari/537.36"
}

for link in links:
    file_url = link.get_attribute('href')

    # Skip links that are not PDFs
    if not file_url.lower().endswith('.pdf'):
        continue

    file_name = file_url.split('/')[-1]  # Get the filename from the URL

    print(f"Downloading {file_name}...")
    try:
        response = requests.get(file_url, headers=headers)
        response.raise_for_status()  # Raise an error if status != 200
        with open(os.path.join(download_folder, file_name), 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_name}: {e}")


# Clean up
driver.quit()

print("All files downloaded!")