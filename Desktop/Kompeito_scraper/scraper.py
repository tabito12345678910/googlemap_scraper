from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

# Specify the path to your ChromeDriver
cdriver = "/Users/tabitosakamoto/Desktop/driver/chromedriver-mac-arm64/chromedriver"
service = Service(cdriver)

# Initialize the WebDriver
#driver specificly retrieving address

location = input("In what city do you want me to scrape? ")
industry = input("In what industry do you want me to scrape? ")
filename = input("What do you want the output csv file to be called? ")
driver = webdriver.Chrome(service=service)
addy_driver = webdriver.Chrome(service=service)
# Navigate to Google Maps
driver.get("https://www.google.com/maps")

# Allow time for the page to load
time.sleep(2)

# Perform a search
search_box = driver.find_element(By.XPATH, "//input[@id='searchboxinput']")
search_box.send_keys(industry + " in " + location)
search_box.send_keys(Keys.RETURN)

# Wait for results to load
time.sleep(2)

# Scrollable div
scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

# JavaScript function to scroll the div
scroll_script = """
var scrollableDiv = arguments[0];
var distance = 1000; // Distance to scroll each time
var scrollDuration = 30000; // Total duration to scroll (in milliseconds)
var startTime = Date.now();

function scrollWithinElement() {
    return new Promise((resolve) => {
        var timer = setInterval(() => {
            var currentTime = Date.now();
            if (currentTime - startTime < scrollDuration) {
                scrollableDiv.scrollBy(0, distance); // Scroll down by the specified distance
            } else {
                clearInterval(timer); // Stop scrolling after the duration
                resolve(); // Resolve the promise
            }
        }, 300); // Delay between each scroll action (in milliseconds)
    });
}

scrollWithinElement();
"""

# Execute the scrolling script
driver.execute_script(scroll_script, scrollable_div)

# Wait for new results to load after scrolling
time.sleep(30)
# Extract the items
items = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction]')

results = []
print(f"Number of items found: {len(items)}")  # Debugging statement

results = []
email_results = []


for item in items:
    data = {}
    email_data = {}
    try: 
        data['phone'] = item.find_element(By.CLASS_NAME, 'UsdlK').text
    except Exception:
        try:
            email_link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') ##changed so it doesnt push a link column
        except Exception:
            pass
        
        try:
            email_data['website'] = addy_driver.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            time.sleep(0.01)
            try:
                addy_driver.get(email_link)
                email_data['address'] = addy_driver.find_element(By.CLASS_NAME, "Io6YTe").text
            except Exception:
                email_data['address'] = location + ", CA"
                pass

            try: 
                email_data['title'] = item.find_element(By.CLASS_NAME, 'qBF1Pd').text
      
            except Exception:
                pass
    
            try: 
                email_data['industry'] = item.find_element(By.CSS_SELECTOR, 'div.W4Efsd > div.W4Efsd > span > span').text
      
            except Exception:
                pass
        except Exception:
            pass
    
        email_data['email'] = '' ##create empty column
    try: 
        data['title'] = item.find_element(By.CLASS_NAME, 'qBF1Pd').text
    
    except Exception:
        pass
    
    try: 
        data['industry'] = item.find_element(By.CSS_SELECTOR, 'div.W4Efsd > div.W4Efsd > span > span').text
    
    except Exception:
        pass
    
    try:
        data['link'] = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    except Exception:
        pass
    try:
        addy_driver.get(data['link'])
        data['address'] = addy_driver.find_element(By.CLASS_NAME, "Io6YTe").text
        data['website'] = addy_driver.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        time.sleep(0.01)
    except Exception:
        data['address'] = location + ", CA"
        pass



    results.append(data)
    email_results.append(email_data)

    


# Convert results to a DataFrame


results[2],results[0] = results[0],results[2]
results[1],results[2] = results[2],results[1]
results[2],results[0] = results[0],results[2]
results[5],results[2] = results[2],results[5]

df = pd.DataFrame(results)
df = df.dropna()
df_email = pd.DataFrame(email_results)
df_email = df_email.dropna()



# Save the DataFrame to a CSV file
df.to_csv(filename + '.csv', index=False)
df_email.to_csv(filename + '_email.csv', index=False)
# Close the browser
addy_driver.quit()
driver.quit()


