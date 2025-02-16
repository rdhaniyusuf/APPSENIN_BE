# servie ini harus selalu akitf dan otomatis logout dan login setiap 20 menit
#  mencegah terjadinya session timeout atau account locked out
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

def process_attendance(driver, name_list, month):
    wait = WebDriverWait(driver, 10)
    all_table_data = {}

    for name in name_list:
        try:
            # Input Nama
            name_input = wait.until(EC.presence_of_element_located((By.XPATH, ".//*/div[2]/div/div[1]/div/div[1]/div/input")))
            name_input.clear()
            name_input.send_keys(name)

            time.sleep(1)
            name_input.click()
            # Tunggu hingga popover muncul
            wait.until(EC.visibility_of_element_located((By.XPATH, 
                                                         "//div[@class='autocomplete']/div[@class='popovers']")))

            # Pilih Opsi
            selected_option = driver.find_element(By.XPATH, "//ul/li[@class='selected']")
            selected_option.click()

            time.sleep(1)  # Delay untuk memastikan data terisi dengan benar

            # Select Bulan
            month_input = wait.until(EC.element_to_be_clickable((By.XPATH, ".//*/div[2]/div/div[1]/div/div[4]/div/input")))
            month_input.click()

            # Pilih Nama Bulan
            month_xpath = f".//*/div/div[2]/div/div[2]/div/div[1]/div/div[4]/div/div/div[2]/div[{month}]"
            select_month = wait.until(EC.element_to_be_clickable((By.XPATH, month_xpath)))
            select_month.click()

            # Klik Button Cari
            search_button = wait.until(EC.element_to_be_clickable((By.XPATH, ".//*/div/div[2]/div/div[2]/div/div[1]/div/div[5]/button")))
            search_button.click()

            time.sleep(2)  # Tunggu data absen muncul

            # Klik Data Absen
            attendance_data = wait.until(EC.element_to_be_clickable((By.XPATH, ".//*/div[2]/div/div[4]/div[1]/div/div/div/div/table/tbody/tr/td[1]")))
            attendance_data.click()

            # Ambil Data dari Tabel
            time.sleep(10)
            header_modal = wait.until(EC.presence_of_element_located((By.XPATH, ".//*/div[2]/div/div[2]/div/div[5]/div/div[1]/div/div/div[1]/div/div[1]")))
            print(f"Data untuk {name} di bulan {month}: {header_modal.text}")
            table = wait.until(EC.presence_of_element_located((By.XPATH, ".//*/div[2]/div/div[2]/div/div[5]/div/div[1]/div/div/div[2]/table")))
            # Save all data from the table
            table_data = []
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td") or row.find_elements(By.TAG_NAME, "th")
                data = [column.text for column in columns]

                try:
                    selected_data = [data[i] for i in [0, 1, 2, 3, 6, 7, 8]]
                    table_data.append(selected_data)
                except IndexError:
                    print(f"Baris tidak memiliki cukup kolom: {data}")
            
            # print(table_data) # You can save this data to a file or a database as needed
            # export_to_sql(name, table_data[1:], output_file=f"{name.lower()}_absen_{minus_date_now.strftime('%Y%m%d')}.sql")
            all_table_data[name] = table_data[1:]
            # Tutup Modal
            close_modal = wait.until(EC.element_to_be_clickable((By.XPATH, ".//*/div/div[2]/div/div[2]/div/div[5]/div/div[1]/div/div/div[1]/div/div[2]/img")))
            close_modal.click()

            time.sleep(1)

        except Exception as e:
            print(f"Gagal memproses data untuk {name}: {e}")
            return None

    return all_table_data


app = FastAPI()

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

def start_service():
    thread = Thread(target=start_browser)
    thread.daemon = True
    thread.start()

@app.lifespan("startup")
def on_startup():
    start_service()