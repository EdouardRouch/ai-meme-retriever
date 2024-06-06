from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import os
import re

def get_driver(headless:bool=True) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://imgflip.com/ai-meme")
    rnd_btn = driver.find_element(By.CLASS_NAME, "aim-meme-btn-random")
    driver.execute_script("arguments[0].style.zIndex=9998;", rnd_btn)
    # Classic Model selection
    driver.find_element(By.XPATH, '//*[@id="aim-wrap"]/div[3]/button[2]').click()
    return driver

def get_meme(driver:webdriver.Chrome, path:str) -> None:
    # Choose random meme template
    driver.find_element(By.CLASS_NAME, "aim-meme-btn-random").click()

    WebDriverWait(driver, 10).until(
        EC.staleness_of(driver.find_element(By.ID, 'site-loading'))
    )
    # Wait 1/2 second to make sure generation is done
    # otherwise greyed out zones can appear in the screenshot
    sleep(.5)
    
    # Center the meme and take a screenshot
    meme_div = driver.find_element(By.XPATH, '//*[@id="aim-preview-wrap"]/div')
    meme_div.location_once_scrolled_into_view
    driver.execute_script("arguments[0].style.zIndex=9999;", meme_div)
    meme_div.screenshot(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AI Meme Retriever')
    parser.add_argument('-n', '--number', type=int, default=1, help='number of memes to retrieve', dest='num_memes')
    parser.add_argument('-p', '--path', type=str, default='./ai-memes', help='path to store the memes', dest='path')

    args = parser.parse_args()

    # Create the folder ai-memes if it does not exist
    os.makedirs(args.path, exist_ok=True)
    abs_path = os.path.abspath(args.path)
    # Get the highest number contained in the memes filename
    meme_files = os.listdir(abs_path)
    highest_number = 0
    for file in meme_files:
        if file.startswith('ai-meme-') and file.endswith('.png'):
            number = int(re.search(r'\d+', file).group())
            highest_number = max(highest_number, number)

    driver = get_driver()
    try:
        for _ in range(args.num_memes):
            highest_number += 1
            meme_path = os.path.join(abs_path, f'ai-meme-{highest_number}.png')
            get_meme(driver, meme_path)
    except Exception as e:
        pass
    finally:
        driver.quit()