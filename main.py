import time
import requests
import sys

import csv
import os

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

# ────────────
# all valid links start with https://www.linkedin.com/jobs/
validLink = "https://www.linkedin.com/jobs/"

# google chrome directory with new settup. loggin once in new profile and selenium keeps session saved
chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\Users\cubos\AppData\Local\Google\Chrome\SeleniumProfile")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--log-level=3")

service = Service("./chromedriver-win64/chromedriver.exe")

# ────────────
while True:
  # 1. get a valid LinkedIn link
  while True:
    mainLink = input("\nPlease enter a valid LinkedIn job Listing you want to scan\n└─")
    try:
      parsedLink = urlparse(mainLink)
      
      # force exception invalid format
      if not (parsedLink.scheme and parsedLink.netloc):
        raise ValueError("Invalid URL format")
      # force exception doesnt have the right format
      if not mainLink.startswith(validLink):
        raise ValueError("Invalid LinkedIn job listing link")
      
      print("\n\INFO\ You entered a valid job listing link\n├─Opening browser and extracting information")
      break
    # exception raises error
    except ValueError:
      print("You entered an invalid job listing link")

# ────────────
  # 2. fetch html content
  response = requests.get(mainLink, headers = {"User-Agent": "Mozilla/5.0"})

  if response.status_code != 200:
    print(f"└─Failed to fetch page. Status code: {response.status_code}")
  else:
    print(f"└─Page fetched Successfuly. Status code: {response.status_code}")
    
    # initialize webdriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(mainLink)
    time.sleep(5)

# ────────────
    # link
    
    # company name
    j_name = driver.find_element(By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__company-name a").text
    # job position
    j_position = driver.find_element(By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__job-title h1 a").text
    # job location
    j_location = driver.find_element(By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__primary-description-container div span span").text

    # job skills button and open
    try:
      svg_element = WebDriverWait(driver, 10).until(
        Ec.presence_of_element_located(
          (By.CSS_SELECTOR, "svg.v-align-middle")
        )
      )
      # debbug. Find the different attribute that defines the button I'm searching for
      # print(f"found svg element ->", svg_element.get_attribute("outerHTML"))

      # from svg with class v-align-middle, crawl up to button
      j_skills_btn = svg_element.find_element(By.XPATH, "./ancestor::button")
      # print(f"found button ->", j_skills_btn.get_attribute("outerHTML")
      # click button
      driver.execute_script("arguments[0].click();", j_skills_btn)
      #print("Clicked the button")

    # exception error handling could not find the button
    except Exception:
      print("Could not load skills button")
    
    # about the job
    j_about = driver.find_element(By.CSS_SELECTOR, "div.jobs-box__html-content").text

# ────────────
    # LINK
    print("Link\n└─", mainLink)
    # FIND company name
    if not j_name:
      print("No COMPANY found")
    else:
      print("Company name\n└─", j_name)
    
    # FIND position
    if not j_position:
      print("No POSITION found")
    else:
      print("Position\n└─", j_position)

    # FIND location
    if not j_location:
      print("No JOB Location found")
    else:
      print("Location\n└─", j_location)

    # FIND skills
    try:
      # skills
      j_skills = WebDriverWait(driver, 10).until(
        Ec.presence_of_all_elements_located((
          By.CSS_SELECTOR, 
          "li.job-details-preferences-and-skills__modal-section-insights-list-item div span"
        ))
      )

      skills = [s.text for s in j_skills if s.text.strip()]

      if not skills:
        print("No SKILLS acossiated with job")
      else:
        print("Skills found")
        for i, skill in enumerate(skills):
          if i < len(skills) -1:
            print("├─", skill)
          else:
            print("└─", skill)

    except Exception:
      print("\ERROR\ Could not load skills")
    
    # FIND job posters info
    j_posters = []
    try:
      # poster name
      j_poster_name_element = WebDriverWait(driver,10).until(
        Ec.presence_of_all_elements_located((
          By.CSS_SELECTOR,
          ".job-details-people-who-can-help__section--two-pane strong"
        ))
      )

      ### job posters format is also under a button that can be clicked to display the same way 
      ### skills is. LATER ON, try to implement functionality for that

      # join posters name and crawl up to a with href of poster linkedin link
      for el in j_poster_name_element:
        name = el.text.strip()
        try:
          link = el.find_element(By.XPATH, "./ancestor::a").get_attribute("href")
        except:
          link = None
        if name:
          j_posters.append((name, link))

      if not j_posters:
        ("No PEOPLE acossiated with the job")
      else:
        # add every person found and respective linkedin link
        print("People found")
        for i, (name, link) in enumerate(j_posters):
          if i < len(j_posters) - 1:
            print("├─", name, "-", link)
          else:
            print("└─", name, "-", link)

    except Exception:
      print("\ERROR -> Could not load people")

    # FIND about
    if not j_about:
      print("No ABOUT SECTION found")
    else:
      print("About Section\n└─", "About the job extracted and saved (Description is too long)")

# ────────────
    jobs_data = []
    last_id = 0

    people, people_link = zip(*j_posters) if j_posters else ([],[])

    job_info = {
      "id": last_id + 1,
      "link": mainLink,
      "company_name": j_name,
      "position": j_position,
      "location": j_location,
      "skills": skills,
      "people": people,
      "people_link": people_link,
      "more_info": j_about
    }
    # add job_info data to jobs_data
    jobs_data.append(job_info)
    # save data into csv file
    csv_file = "jobs_data.csv"
    write_header = not os.path.exists(csv_file)

    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
      writer =  csv.DictWriter(
        f,
        fieldnames=["id","link","company_name","position","location","skills","people","people_link","more_info"]
      )

      if write_header:
        writer.write_header()

      writer.writerow({
        "id": job_info["id"],
        "link": job_info["link"],
        "company_name": job_info["company_name"],
        "position": job_info["position"],
        "location": job_info["location"],
        "skills": "; ".join(job_info["skills"]),        
        "people": "; ".join(job_info["people"]),
        "people_link": "; ".join(job_info["people_link"]),
        "more_info": job_info["more_info"]
      })

# ────────────
  print("\INFO\ Information extracted and saved successfully.")
  
  again = input("\nDo you want to enter another valid LinkedIn job Listing to scan? [Y/n]:").strip().lower()
  if again == "n":
    driver.quit()
    sys.exit(0)
  else:
    driver.quit()
