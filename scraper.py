import bs4
import csv
import time
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import Request, urlopen
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup

file_name = "sl_spirits"
f = open(file_name, "w")
headers = "product_name, product_type, product_size, product_price, retailer, img_url\n"
f.write(headers)

base_url = "https://johnsonville.superliquor.co.nz/"
lk_spirit_types = ["bourbon", "brandy-cognac", "gin", "vodka", "rum", "tequila", "whisky", "liqueurs"]
sl_spirit_types = ["bourbon", "brandy", "gin", "vodka", "rum", "tequila", "whisky", "specialty-liqueur"]


def scrape(spirit, url):
    req = Request(url + spirit, headers={'User-Agent': 'Mozilla/5.0'})
    u_client = urlopen(req)
    page_html = u_client.read()
    u_client.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup


def amount_interpreter(text):

    if "ml" in text:
        string_arr = text.split()
        return string_arr[len(string_arr)-1]
    if "Litre" in text:
        string_arr = text.split()
        return string_arr[len(string_arr)-2] + " " + string_arr[len(string_arr )-1]


def get_contents_lk():

    for spirit in lk_spirit_types:
        # Grabs each product on the page
        html_body = scrape(spirit, base_url)
        containers = html_body.findAll("li", {"class": "catalog-grid-item"})
        for container in containers:
            product_name = container.a.findAll("h2", {"class": "catalog-grid-item__name"})[0].text.strip()
            product_type = spirit
            product_size = container.a.findAll("div", {"class": "catalog-grid-item__pack-size"})[0].text.strip()
            product_price = container.a.findAll("span", {"class": "price"})[0].text.strip()
            img_url = container.a.findAll("div", {"class": "catalog-grid-item__image-wrapper"})[0].img["data-src"]

            f.write(product_name + "," + product_type + "," + product_size + "," + product_price + "," + "Liquor King" + "," + img_url + "\n")
    f.close()


def get_contents_sl():
    for spirit in sl_spirit_types:
        # Grabs each product on the page
        html_body = scrape(spirit, base_url)
        containers = html_body.findAll("div", {"class": "item-box"})
        for container in containers:
            product_name = container.findAll("h2", {"class": "product-title text-uppercase"})[0].text.strip()
            product_type = spirit
            product_size = amount_interpreter(container.findAll("h2", {"class": "product-title text-uppercase"})[0].text.strip())
            product_price = container.findAll("span", {"class": "price actual-price"})[0].text.strip()
            img_url = container.findAll("div", {"class": "picture"})[0].a.img["data-src"]

            f.write(product_name + "," + product_type + "," + product_size + "," + product_price + "," + "Super Liquor" + "," + img_url + "\n")
    f.close()


def main():
    get_contents_sl()


if __name__ == "__main__":
    main()