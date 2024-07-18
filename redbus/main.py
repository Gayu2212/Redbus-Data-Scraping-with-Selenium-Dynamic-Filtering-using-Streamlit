import os
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Function to create SQLite database and table
def create_database():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bus_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS bus_data
                 (bus_route_name TEXT, bus_name TEXT, bus_type TEXT, departure_time TEXT,
                  duration TEXT, arrival_time TEXT, rating TEXT, fare TEXT, seats_available TEXT)''')

    conn.commit()
    conn.close()

# Function to insert data into SQLite
def insert_data(bus_route_name, bus_name, bus_type, departure_time, duration, arrival_time, rating, fare,
                seats_available):
    conn = sqlite3.connect('bus_data.db')
    c = conn.cursor()

    # Insert data into table
    c.execute('''INSERT INTO bus_data (bus_route_name, bus_name, bus_type, departure_time,
                 duration, arrival_time, rating, fare, seats_available)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (bus_route_name, bus_name, bus_type, departure_time, duration, arrival_time, rating, fare,
               seats_available))

    conn.commit()
    conn.close()

# Initialize SQLite database and table
create_database()

# Selenium script to scrape data
def bus(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)
    try:
        dropdown_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".button"))
        )
        dropdown_button.click()
    except TimeoutException:
        print(f"Timeout while waiting for the dropdown button on URL: {url}")
        driver.quit()
        return

    try:
        name = driver.find_element(By.XPATH, '//*[@id="mBWrapper"]/section/div[2]/h1').text
    except NoSuchElementException:
        print(f"No route name found on URL: {url}")
        driver.quit()
        return

    # Scroll down the page to load more content
    scroll_pause_time = 2  # Adjust as needed
    screen_height = driver.execute_script("return window.screen.height;")  # Get the screen height of the web

    i = 1
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == screen_height or i > 5:  # Adjust the number of scrolls or conditions as needed
            break
        screen_height = new_height
        i += 1

    try:
        # Find the result section
        result_section = driver.find_element(By.ID, "result-section")

        # Find all bus items
        bus_items = result_section.find_elements(By.CLASS_NAME, "bus-item")
        processed_count = 0

        # Check if bus_items is empty
        if not bus_items:
            print("No Data Found")
        else:
            # Loop through each bus item and extract data
            for bus in bus_items:
                if processed_count >= 10:
                    break

                try:
                    bus_name = bus.find_element(By.CLASS_NAME, "travels").text
                    bus_type = bus.find_element(By.CLASS_NAME, "bus-type").text
                    departure_time = bus.find_element(By.CLASS_NAME, "dp-time").text
                    duration = bus.find_element(By.CLASS_NAME, "dur").text
                    arrival_time = bus.find_element(By.CLASS_NAME, "bp-time").text
                    rating = bus.find_element(By.CLASS_NAME, "rating").text
                    fare = bus.find_element(By.CLASS_NAME, "fare").text.replace('INR', '').strip()
                    seats_available = bus.find_element(By.CLASS_NAME, "seat-left").text

                    # Insert data into SQLite
                    insert_data(name, bus_name, bus_type, departure_time, duration, arrival_time, rating, fare, seats_available)

                    # Print or store the extracted data
                    print(f"Bus Route Name: {name}")
                    print(f"Bus Name: {bus_name}")
                    print(f"Bus Type: {bus_type}")
                    print(f"Departure Time: {departure_time}")
                    print(f"Duration: {duration}")
                    print(f"Arrival Time: {arrival_time}")
                    print(f"Rating: {rating}")
                    print(f"Fare: {fare}")
                    print(f"Seats Available: {seats_available}")
                    print("\n")

                    # Increment the counter
                    processed_count += 1

                except Exception as e:
                    print(f"Error extracting bus data: {e}")

    except NoSuchElementException:
        print(f"No result section found on URL: {url}")

    driver.quit()

def stateBus(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(10)

    elements = driver.find_elements(By.XPATH, "//a[@class='route' and contains(@title, 'to')]")

    # Extract and print the href attribute for each element
    for element in elements:
        href = element.get_attribute('href')
        bus(href)
        print(href)
    driver.quit()

driver = webdriver.Chrome()
driver.get("https://www.redbus.in/")
driver.maximize_window()
driver.implicitly_wait(10)

# Navigate to the specified link
name = driver.find_element(By.XPATH, '//*[@id="homeV2-root"]/div[3]/div[1]/div[2]/a')
val = name.get_attribute('href')
driver.get(val)
driver.maximize_window()

parent_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/article[2]/div/div')
links = parent_element.find_elements(By.TAG_NAME, 'a')

# Extract and print the href attribute of each link
for link in links:
    href = link.get_attribute('href')
    print(href)
    stateBus(href)

# Quit the driver
driver.quit()
