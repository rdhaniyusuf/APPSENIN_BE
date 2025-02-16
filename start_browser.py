import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from fastapi import FastAPI
from threading import Thread

# Set Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without UI
chrome_options.add_argument("--window-size=1920,1080") # Window size
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
)

DATE_NOW = datetime.datetime.now().date()

DRIVER = None

def start_browser():
    while True:
        # Initialize ChromeDriver with webdriver_manager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        # Get URL from environment variable
        url = os.getenv("ABSEN_LINK")
        driver.get(url)

        # Find the username and password input fields and the login button
        username_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, ".//*/form/div[3]/div/input"))
        )
        time.sleep(1)
        username_input.send_keys(os.getenv("USER_NAME_LINK"))

        password_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, ".//*/form/div[4]/div/div/input"))
        )
        time.sleep(1)
        password_input.send_keys(os.getenv("PASSWORD_LINK"))

        login_button = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, ".//*/form/div[5]/div/button"))
        )
        time.sleep(1)
        login_button.click()

        # Wait for the login to complete
        time.sleep(10)
        # klik menu absen kehadiran
        kehadiran_menu = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, ".//*/div[1]/div[1]/ul/div[2]/div[1]/div"))
        )
        time.sleep(2)
        kehadiran_menu.click()

        # Perform your attendance processing here
        # Example: process_attendance(driver, ["Name1", "Name2"], 1)

        DRIVER = driver

        # Wait for 20 minutes before logging out and logging in again
        time.sleep(20 * 60)

        # button logout
        logout_button = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, ".//header/ul[2]/li[2]/div/a"))
        )
        logout_button.click()

        # Close the browser
        driver.quit()