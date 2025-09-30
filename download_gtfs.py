import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os

page_url = "https://www.metrodoporto.pt/pages/337"

response = requests.get(page_url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

li = soup.find("li", class_=lambda c: c and "last zip" in c)
if li is None:
    raise ValueError("Could not find the latest GTFS link")

a_tag = li.find("a")
if a_tag is None or "href" not in a_tag.attrs:
    raise ValueError("No <a> tag with href found inside the <li>")

gtfs_url = urljoin(page_url, a_tag["href"])
print("Found GTFS URL:", gtfs_url)

gtfs_response = requests.get(gtfs_url)
gtfs_response.raise_for_status()

filename = "gtfs_metroporto_latest.zip"
with open(filename, "wb") as f:
    f.write(gtfs_response.content)

print(f"Downloaded GTFS file as {filename}")

