from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sqlite3
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def createDatabase():
    connection=sqlite3.connect('busdatas.db')
    c=connection.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS andhra_bus
                 (bus_route_name TEXT, bus_name TEXT, bus_type TEXT, departure_time TEXT,
                  duration TEXT, arrival_time TEXT, rating TEXT, fare TEXT, seats_available TEXT)''')
    connection.commit()
    connection.close()

def insert_data(name, bus_name, bus_type, departure_time, duration, arrival_time, rating, fare, seats_available):
    connection=sqlite3.connect('busdatas.db')
    c=connection.cursor()
    c.execute('''INSERT INTO andhra_bus (bus_route_name, bus_name, bus_type, departure_time,
                 duration, arrival_time, rating, fare, seats_available)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (name, bus_name, bus_type, departure_time, duration, arrival_time, rating, fare,
               seats_available))
    
    connection.commit()
    connection.close()

createDatabase()




def bus(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.minimize_window
    driver.implicitly_wait(10)
    dropdown_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".button"))
    )
    dropdown_button.click()

    name = driver.find_element(By.XPATH, '//*[@id="mBWrapper"]/section/div[2]/h1').text

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

    # Find the result section
    result_section = driver.find_element(By.ID, "result-section")

    # Find all bus items
    bus_items = result_section.find_elements(By.CLASS_NAME, "bus-item")

    # Loop through each bus item and extract data
    for bus in bus_items:
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
        except Exception as e:
            print(f"Error extracting bus data: {e}")

    driver.quit()




driver = webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/apsrtc/")
driver.maximize_window()
driver.implicitly_wait(10)

elements = driver.find_elements(By.XPATH, "//a[@class='route' and contains(@title, 'to')]")

# Extract and print the href attribute for each element
for element in elements:
    href = element.get_attribute('href')
    bus(href)
    print(href)

