import time
import requests

import webbrowser as wb
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By

print(r"""
    ___       ___       ___       ___       ___       ___       ___   
   /\  \     /\__\     /\  \     /\  \     /\  \     /\  \     /\  \  
  /  \  \   / /__/_   _\ \  \   /  \  \    \ \  \   /  \  \   /  \  \ 
 /\ \ \__\ /  \/\__\ /\/  \__\ /  \ \__\   /  \__\ /  \ \__\ /  \ \__\
 \ \ \/__/ \/\  /  / \  /\/__/ \/\ \/__/  / /\/__/ \ \ \/__/ \;   /  /
  \  /  /    / /  /   \ \__\      \/__/   \/__/     \ \/__/   | \/__/ 
   \/__/     \/__/     \/__/                         \/__/     \|__|  
""")
print("\n*********************************************************************")
print("\n* Original Code by Shifter                                          *")
print("\n* LinkedIn Job Post Scanner                                         *")
print("\n*********************************************************************")

# all valid links start with https://www.linkedin.com/jobs/
validLink = "https://www.linkedin.com/jobs/"
driver = webdriver.Chrome()

while True:
  # 1. get a valid LinkedIn link
  while True:
    mainLink = input("\nPlease enter a valid LinkedIn job Listing you want to scan:\n->")
    try:
      parsedLink = urlparse(mainLink)
      
      # force exception invalid format
      if not (parsedLink.scheme and parsedLink.netloc):
        raise ValueError("Invalid URL format")
      # force exception doesnt have the right format
      if not mainLink.startswith(validLink):
        raise ValueError("Invalid LinkedIn job listing link")
      
      print("\nYou entered a valid job listing link\nOpening browser and extracting information")
      break
    # exception raises error
    except ValueError:
      print("You entered an invalid job listing link")

  # open if link passes validation
  wb.open(mainLink)

  # 2. fetch html content
  response = requests.get(mainLink, headers = {"User-Agent": "Mozilla/5.0"})
  if response.status_code != 200:
    print(f"Failed to fetch page. Status code: {response.status_code}")
  else:
    print(f"Page fetched Successfuly. Status code: {response.status_code}")
    
    driver.get(mainLink)
    time.sleep(5)
    # find divs
    divs = driver.find_elements(By.CLASS_NAME, "application-outlet")

    if not divs:
      print("No div found")
    else:
      print("DIV FOUND")
    
    driver.quit()

  while True:
    pass