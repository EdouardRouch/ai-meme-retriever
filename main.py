from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("https://imgflip.com/ai-meme")

# Classic Model selection
driver.find_element(By.XPATH, '//*[@id="aim-wrap"]/div[3]/button[2]').click()
# Choose random meme template
driver.find_element(By.CLASS_NAME, "aim-meme-btn-random").click()

try:
    # Wait for the meme to be generated
    WebDriverWait(driver, 10).until_not(
        EC.text_to_be_present_in_element_attribute((By.XPATH, '//*[@id="aim-preview-wrap"]/div/canvas'), "width", "300")
    )
    # Wait /2 second to make sure the meme is fully loaded 
    # (otherwise their is sometimes greyed out parts)
    sleep(.5)
    
    # Center the meme and take a screenshot
    meme = driver.find_element(By.XPATH, '//*[@id="aim-preview-wrap"]/div')
    meme.location_once_scrolled_into_view
    driver.execute_script("arguments[0].style.zIndex=9999;", meme)
    meme.screenshot("meme.png")
finally:
    driver.quit()

