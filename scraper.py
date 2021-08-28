import bs4
import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

file_name = "lk_spirits"
f = open(file_name, "w")
headers = "product_name, product_type, product_size, product_price, retailer img_url\n"
f.write(headers)

base_url = "https://www.lk.co.nz/spirits/"
spirit_types = ["bourbon", "brandy-cognac", "gin", "vodka", "rum", "tequila", "whisky", "liqueurs"]
for spirit in spirit_types:
    # print("============================================")
    # print(spirit)
    # print("============================================")
    req = Request(base_url+spirit, headers={'User-Agent': 'Mozilla/5.0'})
    u_client = urlopen(req)
    page_html = u_client.read()
    u_client.close()
    page_soup = soup(page_html, "html.parser")
    header = page_soup.h1

    # Grabs each product on the page
    containers = page_soup.findAll("li", {"class": "catalog-grid-item"})
    for container in containers:
        product_name = container.a.findAll("h2", {"class": "catalog-grid-item__name"})[0].text.strip()
        product_type = spirit
        product_size = container.a.findAll("div", {"class": "catalog-grid-item__pack-size"})[0].text.strip()
        product_price = container.a.findAll("span", {"class": "price"})[0].text.strip()
        img_url = container.a.findAll("div", {"class": "catalog-grid-item__image-wrapper"})[0].img["data-src"]

        f.write(product_name + "," + product_type + "," + product_size + "," + product_price + "," + "Liquor King" + "," + img_url + "\n")
f.close()