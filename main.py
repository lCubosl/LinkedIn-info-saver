import webbrowser as wb
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

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

while True:
  # 1. get a valid LinkedIn link
  while True:
    linkedInLink = input("\nPlease enter a valid LinkedIn job Listing you want to scan:\n->")
    try:
      parsedLink = urlparse(linkedInLink)
      
      # force exception invalid format
      if not (parsedLink.scheme and parsedLink.netloc):
        raise ValueError("Invalid URL format")
      # force exception doesnt have the right format
      if not linkedInLink.startswith(validLink):
        raise ValueError("Invalid LinkedIn job listing link")
      
      print("\nYou entered a valid job listing link\nOpening browser and extracting information")
      break
    # exception raises error
    except ValueError:
      print("You entered an invalid job listing link")

  # open if link passes validation
  wb.open(linkedInLink)

  while True:
    pass