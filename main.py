import re
import requests
import csv

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
        urls = urls + find_fliter_urls(html_text, url_pattern)
        url_pattern = re.compile(r'href=["\'](https://www\.supercars\.net/blog/\d[^-]+-' + re.escape(call_in_layer) + r'[^/]+/)["\']')
        urls = urls + find_fliter_urls(html_text, url_pattern)
        return urls
    elif layer == 3:
        url_pattern
    
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
        if re.sub(r'<[^>]+>', '', data_rows[0]).strip() == "": continue
        ret.append(f"{re.sub(r'<[^>]+>', '', data_rows[0]).strip()} : {re.sub(r'<[^>]+>', '', data_rows[1]).strip()}")
    return " | ".join(ret)

def scrape():
    all_urls = []
    letter_str = input("Put in the alphabet :")
    html_url = html_base + letter_str.lower() + "/"
    html_content = fetch_html(html_url)
    
    car_urls = filter_url(html_content, 2, letter_str)
    
    for url in car_urls:
        all_urls.append([url, find_table(url=url)])


    
    with open(f'./csv/car_brands_urls_with_letter{letter_str.lower()}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_urls)

while True:
    scrape()