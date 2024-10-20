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
driver = webdriver.Chrome(service=service)

location = input("In what city do you want me to scrape? ")
industry = input("In what industry do you want me to scrape? ")
filename = input("What do you want the output csv file to be called? ")

# Navigate to Google Maps
driver.get("https://www.google.com/maps")
try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2)"))).click()
except Exception:
    pass

# Allow time for the page to load
time.sleep(5)

# Perform a search
search_box = driver.find_element(By.XPATH, "//input[@id='searchboxinput']")
search_box.send_keys(industry + " in " + location)
search_box.send_keys(Keys.RETURN)

# Wait for results to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
)

# Scrollable div
scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

# JavaScript function to scroll the div
scroll_script = """
var scrollableDiv = arguments[0];
var totalHeight = 0;
var distance = 500; // Distance to scroll each time
var scrollDelay = 3000; // Delay between scrolls

function scrollWithinElement() {
    return new Promise((resolve) => {
        var timer = setInterval(() => {
            var scrollHeightBefore = scrollableDiv.scrollHeight;
            scrollableDiv.scrollBy(0, distance);
            totalHeight += distance;

            if (totalHeight >= scrollHeightBefore) {
                clearInterval(timer); // Stop scrolling
                resolve(); // Resolve the promise
            }
        }, scrollDelay);
    });
}

scrollWithinElement();
"""

# Execute the scrolling script
driver.execute_script(scroll_script, scrollable_div)

# Wait for new results to load after scrolling
time.sleep(60)
# Extract the items
items = driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction]')

results = []
print(f"Number of items found: {len(items)}")  # Debugging statement

results = []


for item in items:
    data = {}
    try: 
        data['title'] = item.find_element(By.CLASS_NAME, 'qBF1Pd').text
      
    except Exception:
        pass
    
    try: 
        data['industry'] = item.find_element(By.CSS_SELECTOR, 'div.W4Efsd > div.W4Efsd > span > span').text
      
    except Exception:
        pass
    
    try: 
        data['phone'] = item.find_element(By.CLASS_NAME, 'UsdlK').text
    except Exception:
        pass
    

    try:
        data['address'] = location + ", CA"
    except Exception:
        pass

    results.append(data)

    


# Convert results to a DataFrame


results[2],results[0] = results[0],results[2]
results[1],results[2] = results[2],results[1]
df = pd.DataFrame(results)


# Save the DataFrame to a CSV file
df.to_csv(filename + '.csv', index=False)
# Close the browser
driver.quit()


