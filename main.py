from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

url = "https://appbrewery.github.io/Zillow-Clone/"
form_url = "https://docs.google.com/forms/d/e/1FAIpQLScsESx6SNsbCbpV2MzYbpBzv3Wc6t6ePTAit9QRZK1GAwg2nw/viewform?usp=header"
responses_url = "https://docs.google.com/forms/d/1Xx7MahJ_TLhVVDsBLVoUXRaFSv6IB2llx-RdwEiir2A/edit#responses"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.text, "html.parser")

#print(soup.prettify())

link_elements = soup.select(".StyledPropertyCardDataWrapper a")
links = [link["href"] for link in link_elements]

#print(f"There are {len(links)} links to individual listings in total: \n")
#print(links)

price_elements = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
prices = [price.get_text().replace("/mo", "").split("+")[0] for price in price_elements]

#print(f"There are {len(prices)} prices to individual listings in total: \n")
#print(prices)

address_elements = link_elements = soup.select("address")
addresses = [address.get_text().replace(" | ", " ").strip() for address in address_elements]

#print(f"There are {len(addresses)} addresses to individual listings in total: \n")
#print(addresses)

chrome_options = webdriver.ChromeOptions()
# Keep chrome browser open after program finishes
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)

for i in range(2):
    driver.get(form_url)
    time.sleep(2)
    inputs = driver.find_elements(By.CLASS_NAME, "whsOnd")
    inputs[0].send_keys(addresses[i])
    inputs[1].send_keys(prices[i])
    inputs[2].send_keys(links[i])
    driver.find_element(By.CLASS_NAME, "NPEfkd").click()
    time.sleep(2)

driver.get(responses_url)
time.sleep(2)
driver.find_element(By.CLASS_NAME, "NPEfkd").click()



