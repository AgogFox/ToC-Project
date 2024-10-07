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
        url_pattern = re.compile(
            r'href=["\'](https://www\.supercars\.net/blog/all-car-brands-a-to-z/[a-z]/)["\']')
    elif layer == 2:
        url_pattern = re.compile(
            r'href=["\'](https://www\.supercars\.net/blog/' + re.escape(call_in_layer) + r'[^/]+/)["\']')
        urls = find_fliter_urls(html_text, url_pattern)
        url_pattern = re.compile(
            r'href=["\'](https://www\.supercars\.net/blog/tag/' + re.escape(call_in_layer) + r'[^/]+/)["\']')
        urls = urls + find_fliter_urls(html_text, url_pattern)
        url_pattern = re.compile(
            r'href=["\'](https://www\.supercars\.net/blog/\d[^-]+-' + re.escape(call_in_layer) + r'[^/]+/)["\']')
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
    pattern = re.compile(
        r'<table class="cardetails"[^>]*>(.*?)</table>', re.DOTALL)
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
        ret.append(
            f"{re.sub(r'<[^>]+>', '', data_rows[0]).strip()} : {re.sub(r'<[^>]+>', '', data_rows[1]).strip()}")
    return " | ".join(ret)

def find_car(url):
    ret = []
    print(f"Processing {url}...")
    pattern = re.compile(
        r'<div class="mask">.*?</div>\s*<div class="meta">(.*?)</div>', re.DOTALL
    )

    html_content = fetch_html(url)
    matches = pattern.findall(html_content)

    if not matches:
        return []

    for wrap in matches:
        if re.search(r'<div class="byline">', wrap, re.IGNORECASE):
            continue

        title_pattern = re.compile(
            r'<h3 class="title"><a [^>]*href="(.*?)">(.*?)</a></h3>', re.DOTALL
        )
        match = title_pattern.search(wrap)
        if match:
            car_url = match.group(1)
            car_title = match.group(2)
            if "gallery" in car_title.lower():
                continue
            print(f"From {url} added {car_url}")
            ret.append([car_url, find_table(car_url)])
    return ret

def scrape():
    all_urls = []
    letter_str = input("Put in the alphabet :")
    html_url = html_base + letter_str.lower() + "/"
    html_content = fetch_html(html_url)

    car_urls = filter_url(html_content, 2, letter_str)

    for url in car_urls:
        table = find_table(url=url)
        if table is None:
            all_urls += find_car(url)
        else:
            print(f"From {url} added something")
            all_urls.append([url, table])

    with open(f'car_brands_urls_with_letter{letter_str.lower()}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(all_urls)

while True:
    scrape()