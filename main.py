import time
import requests

from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec

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

# google chrome directory with new settup. loggin once in new profile and selenium keeps session saved
chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\Users\cubos\AppData\Local\Google\Chrome\SeleniumProfile")

service = Service("./chromedriver-win64/chromedriver.exe")

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

  # 2. fetch html content
  response = requests.get(mainLink, headers = {"User-Agent": "Mozilla/5.0"})
  if response.status_code != 200:
    print(f"Failed to fetch page. Status code: {response.status_code}")
  else:
    print(f"Page fetched Successfuly. Status code: {response.status_code}")
    
    # initialize webdriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(mainLink)
    time.sleep(5)
    
    # company name
    j_name = driver.find_element(By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__company-name a").text
    # job position
    j_position = driver.find_element(By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__job-title h1 a").text
    
    # job skills button and open
    try:
      svg_element = WebDriverWait(driver, 10).until(
        Ec.presence_of_element_located(
          (By.CSS_SELECTOR, "svg.v-align-middle")
        )
      )
      # debbug. Find the different attribute that defines the button I'm searching for
      print(f"found svg element ->", svg_element.get_attribute("outerHTML"))

      # from svg with class v-align-middle, crawl up to button
      j_skills_btn = svg_element.find_element(By.XPATH, "./ancestor::button")
      print(f"found button ->", j_skills_btn.get_attribute("outerHTML"))


    except Exception:
      print("Could not load skills button")

    try:
      # skills
      j_skills = WebDriverWait(driver, 10).until(
        Ec.presence_of_all_elements_located(
          By.CSS_SELECTOR, 
          "li.job-details-preferences-and-skills__modal-section-insights-list-item div span"
        )
      )

      skills = [s.text for s in j_skills if s.text.strip()]

      if skills:
        print("Skills found")
        for skill in skills:
          print("->", skill)
        else:
          print("No SKILLS acossiated with job")
    except Exception:
      print("Could not load skills")

    # find company name
    if not j_name:
      print("No COMPANY found")
    else:
      print("Company name ->", j_name)
    
    # find position
    if not j_position:
      print("No POSITION found")
    else:
      print("Position ->", j_position)

    driver.quit()

  while True:
    pass