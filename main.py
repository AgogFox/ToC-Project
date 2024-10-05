import re
import requests
import csv
import json

html_base = "https://www.supercars.net/blog/all-car-brands-a-to-z/"

def fetch_html(html):
    return requests.get(html).text

def filter_url(html_text, layer, call_in_layer=None):
    if layer == 0:
        url_pattern = re.compile(r'href=["\'](http[s]?://[^"\']+)["\']')
    elif layer == 1:
        url_pattern = re.compile(r'href=["\'](https://www\.supercars\.net/blog/all-car-brands-a-to-z/[a-z]/)["\']')
    elif layer == 2:
        url_pattern = re.compile(r'href=["\'](https://www\.supercars\.net/blog/' + re.escape(call_in_layer) + r'[^/]+/)["\']')
        urls = find_fliter_urls(html_text, url_pattern)
        url_pattern = re.compile(r'href=["\'](https://www\.supercars\.net/blog/tag/' + re.escape(call_in_layer) + r'[^/]+/)["\']')
        urls += find_fliter_urls(html_text, url_pattern)
        url_pattern = re.compile(r'href=["\'](https://www\.supercars\.net/blog/\d[^-]+-' + re.escape(call_in_layer) + r'[^/]+/)["\']')
        urls += find_fliter_urls(html_text, url_pattern)
        return urls

    urls = find_fliter_urls(html_text, url_pattern)
    return urls

def find_fliter_urls(html_text, url_pattern):
    urls = url_pattern.findall(html_text)
    urls = list(set(urls))
    urls.sort()
    return urls

def find_table(url):
    ret = []
    pattern = re.compile(r'<table class="cardetails"[^>]*>(.*?)</table>', re.DOTALL)
    match = pattern.search(fetch_html(url))
    if not match:
        return None
    
    table = match.group(1)
    pattern = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
    rows = pattern.findall(table)

    for row in rows:
        pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL)
        data_rows = pattern.findall(row)
        if re.sub(r'<[^>]+>', '', data_rows[0]).strip() == "":
            continue
        ret.append(f"{re.sub(r'<[^>]+>', '', data_rows[0]).strip()} : {re.sub(r'<[^>]+>', '', data_rows[1]).strip()}")
    return " | ".join(ret)

def scrape():
    all_urls = []
    letter_str = input("Put in the alphabet: ")
    html_url = html_base + letter_str.lower() + "/"
    html_content = fetch_html(html_url)
    
    car_urls = filter_url(html_content, 2, letter_str)
    
    for url in car_urls:
        all_urls.append([url, find_table(url=url)])

    csv_file = f'car_brands_urls_with_letter{letter_str.lower()}.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(all_urls)

    json_file = f'car_brands_urls_with_letter{letter_str.lower()}.json'
    data = []
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            url = row[0]
            details = row[1] if len(row) > 1 else ""
            
            details_dict = {}
            if details:
                pairs = details.split(" | ")
                for pair in pairs:
                    if ":" in pair:
                        key, value = pair.split(":", 1)
                        details_dict[key.strip()] = value.strip()
                    else:
                        details_dict[pair.strip()] = ""

            item = {"url": url}
            item.update(details_dict)
            data.append(item)
    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

while True:
    scrape()
