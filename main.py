import re
import requests
import json
from flask import Flask, request, send_from_directory
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://www.supercars.net/blog/all-brands/"

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
        brands = [(item[0], item[1].replace("&amp;", "&").replace("...", ".").replace("..", ".").replace("..", ".")) for item in brands]
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
    
    def find_header(self, self_url: str) -> str: 
        pattern = re.compile(
            r'<h1 class="entry-title[^>]*>(.*?)<\/h1>'
        )
        self_html = self.__fetch_html(self_url)
        match = re.search(pattern, self_html)
        if match:
            header = match.group(1).strip() 
        else:
            header = None
        return header

app = Flask(__name__)
scraper = Scraper(BASE_URL)

@app.route('/')
def home():
    return send_from_directory('www/home','index.html')

@app.route('/brands')
def send_brands_file():
    return send_from_directory('www/brands', 'brands.html')

@app.route('/models')
def send_models_file():
    return send_from_directory('www/models', 'models.html')

@app.route('/api/alpha/<char>', methods=["GET"])
def alphabet(char):
    names = list(scraper.find_brands_list(char).keys()) #First layer
    r = {char : names}
    return r

@app.route('/api/brand/<name>', methods=["GET"])
def brand(name):
    r = {}
    first_letter = name[0].upper()

    # First layer: Fetching the brand dictionary
    brands_dict = scraper.find_brands_list(first_letter)
    brand_url = brands_dict[name.upper()]  # Second layer: Brand URL

    # Fetch all models (Third layer)
    models = scraper.find_model(brand_url)

    # Function to fetch model table
    def fetch_model_table(model_name, model_url):
        return model_name, scraper.find_table(model_url)
    
    def fetch_self_table(self_url):
        return scraper.find_header(self_url), scraper.find_table(self_url)

    # Use ThreadPoolExecutor for parallel fetching of model tables
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_model_table, model_name, model_url) 
                    for model_name, model_url in models.items()]
        self_futures = executor.submit(fetch_self_table, brand_url)

        # Gather results from all threads
        for future in as_completed(futures + [self_futures]):
            model_name, table_data = future.result()
            r[model_name] = table_data
            
    return r

@app.route('/api/search', methods=["GET"])
def search():
    query = request.args.get('q').lower()
    result_model = {}
    result = {}

    # First multithreading to fetch brand lists
    brands_az_dict = {}
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(scraper.find_brands_list, chr(i)): i for i in range(65, 90)}
        for future in as_completed(futures):
            i = futures[future]
            try:
                brands_az_dict[i] = future.result()
            except Exception as e:
                print(f"Failed to fetch brands for letter {chr(i)}: {e}")

    # Now, gather all the brand links and find models for each brand
    with ThreadPoolExecutor() as executor:
        model_futures = []
        for brand_alpha in brands_az_dict.values():  # brand a-z
            for brand in brand_alpha.values():  # link to each brand
                # Queue up a thread to find models for each brand
                model_futures.append(executor.submit(scraper.find_model, brand))
        
        for future in as_completed(model_futures):
            try:
                models = future.result()
                # Filter models based on the query and update result_model
                result_model.update({k: v for k, v in models.items() if query in k.lower()})
            except Exception as e:
                print(f"Failed to fetch models: {e}")

    # Finally, multithreading to find tables for each model
    with ThreadPoolExecutor() as executor:
        table_futures = {executor.submit(scraper.find_table, model_url): model_name for model_name, model_url in result_model.items()}
        for future in as_completed(table_futures):
            model_name = table_futures[future]
            try:
                result[model_name] = future.result()
            except Exception as e:
                print(f"Failed to fetch table for {model_name}: {e}")

    return result

if(__name__) == "__main__":
    app.run(debug=True, host="0.0.0.0")