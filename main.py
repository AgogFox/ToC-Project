import re
import requests
import json
from flask import Flask

BASE_URL = "https://www.supercars.net/blog/all-brands/"

#TODO
#[x]filter brands base on alphabet
#filter car of each brand
#   [x]301 to all-brands
#   [x]301 to /blog/category
#   [x] direct
#   [] 301 manual
#[x]filter infomation of each car
#[]create API endpoint
#[x]convert return data to json format agreed on API docs
#[]scrape image
#[]search
#[]convert data to csv for download
#[]filter everything before 'Pictures &amp; Galleries' for easier scraping
#[]click load more button to get full information

class Scraper:
    def __init__(self, url: str) -> None:
        self.BASE_URL = url
        self.BASE_HTML = self.__fetch_html(self.BASE_URL)

    def __fetch_html(self, url):
        return requests.get(url).text

    def find_brands_list(self, char: str) -> dict: #First layer: find list of brands
        brand_dict = {}
        brand_pattern = re.compile(
            rf'<li><p><a[^>]*\bhref=["\']([^"\']*)["\'][^>]*>({char.upper()}.*?)</a>'
        )
        brands = re.findall(brand_pattern, self.BASE_HTML)
        for brand_url, brand_name in brands:
            brand_dict[brand_name] = brand_url
        return brand_dict

    def find_model(self, brand_url: str) -> dict: #Second layer: find list of cars in that brand
        models_dict = {}
        models = []
        card_pattern = re.compile(
            r'<div class="mask">.*?</div>\s*<div class="meta">(.*?)</div>', re.DOTALL
        )
        brand_html = self.__fetch_html(brand_url)

        cards = card_pattern.findall(brand_html)
        
        if cards is None:
            return []
        
        for card in cards: 
            
            if re.search(r'<div class="byline">', card, re.IGNORECASE): #skip articles cards
                continue
            
            card_title_pattern = re.compile(
                r'<h3 class="title"><a [^>]*href="(.*?)">(.*?)</a></h3>', re.DOTALL
            )

            card_title = card_title_pattern.search(card)
            if card_title:
                model_url = card_title.group(1)
                model_title = card_title.group(2)
                
                if "gallery" in model_title.lower(): #skip if it is a gallery
                    continue
                
                models.append((model_title, model_url))
        
        for model_name, model_url in models:
            models_dict[model_name] = model_url

        return models_dict

    def __find_image(self, html: str) -> dict:
        image_pattern = re.compile(
            r'<div class="hero">.*?<img [^>]*src="([^"]+)"[^>]*>.*?</div>'
        )
        image_url = image_pattern.search(html)
        return image_url.group(1)

    def find_table(self, model_url: str) -> dict: #Third layer: find infomation of that car
        table_dict = {}
        table = []
        table_pattern = re.compile(
            r'<table class="cardetails"[^>]*>(.*?)</table>', re.DOTALL
        )

        model_html = self.__fetch_html(model_url)
        table_html = table_pattern.search(model_html)
        image_url = self.__find_image(model_html)
        table_dict["img"]  = image_url

        if table_html is None:
            return
        
        table_html = table_html.group(0) #extract html from match object
        row_pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
        rows = row_pattern.findall(table_html)

        for row in rows:
            data_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL)
            data_column = data_pattern.findall(row)

            if re.sub(r'<[^>]+>', '', data_column[0]).strip() == "": #skip if the first column is empty
                continue

            table.append(
                re.sub(r'<[^>]+>', '', data_column[0]).strip() + " : " + 
                re.sub(r'<[^>]+>', '', data_column[1]).strip()
            )

        for item in table:
            key, value = item.split(' : ')
            table_dict[key] = value
        return table_dict

app = Flask(__name__)
scraper = Scraper(BASE_URL)


@app.route('/api/alpha/<char>', methods=["GET"])
def alphabet(char):
    names = list(scraper.find_brands_list(char).keys()) #First layer
    r = {char : names}
    return r

@app.route('/api/brand/<name>', methods=["GET"])
def brand(name):
    r = {}
    first_letter = name[0]
    brands_dict = scraper.find_brands_list(first_letter) #First layer
    brand_url = brands_dict[name.upper()] #Seccond layer
    models = scraper.find_model(brand_url)
    for model_name, model_url in models.items():
        r[model_name] = scraper.find_table(model_url) #Third layer
    return r


def search():
    pass

if(__name__) == "__main__":
    app.run(debug=True)