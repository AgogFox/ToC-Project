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

        raw_data = find_table(url=url)
        data_clened = clean_data(raw_data)
        all_urls.append([url, data_clened])

    
    with open(f'./csv/car_brands_urls_with_letter{letter_str.lower()}.csv', mode='w', newline='') as file:

        writer = csv.writer(file)
        writer.writerows(all_urls)






def clean_data(raw_data) -> str:

    black_lists = ["&#", "&nbsp", "\n", "gear ratios", "8211"]

    return_str = ""

    if type(raw_data) == str:
            
            key_value_list = raw_data.split("|")

            for each_field in key_value_list:       #[" price $ : $31 860 ", " engine : Chev V8 "]

                each_field_list = each_field.split(':')

                key = each_field_list[0]
                value = each_field_list[1]



                found_black_list_word = False

                # Remove HTML tags
                key = re.sub(r'<[^>]+>', '', key)
    
                # Remove URL-encoded characters
                key = re.sub(r'%[0-9A-Fa-f]{2}', ' ', key)

                # Normalize whitespace
                key = re.sub(r'\s+', ' ', key).strip()

                # Remove special characters except alphanumeric and spaces
                key = re.sub(r'[^a-zA-Z0-9\s\$]', '', key)

                # Remove specific patterns like $digit between alphabetic characters
                key = re.sub(r'(?<=[a-zA-Z])\$\d(?=[a-zA-Z])', '', key)



                # Remove HTML tags
                value = re.sub(r'<[^>]+>', '', value)

                # Remove URL-encoded characters
                value = re.sub(r'%[0-9A-Fa-f]{2}', ' ', value)

                # Normalize whitespace
                value = re.sub(r'\s+', ' ', value).strip()

                # Remove special characters except alphanumeric and spaces
                value = re.sub(r'[^a-zA-Z0-9\s\$³²\–,~/]', '', value)

                # Remove specific patterns like $digit between alphabetic characters
                value = re.sub(r'(?<=[a-zA-Z])\$\d(?=[a-zA-Z])', '', value)


                # replace string
                key = re.sub("^\s+", "", key)    # REPLACE WHITE SPACE IN FRONT OF KEY

                value = re.sub('Â', '', value)

                #Special case
                value = re.sub("(?<=[a-zA-Z])\$\d*(?=[a-zA-Z])", '', value)

                if(re.search("price", key)):
                    key = re.sub(".*price.*", "price", key)
                    value = re.sub("[^\d]", "", value)

                if(re.search("^ $", value) or re.search("^ $", key)):
                    found_black_list_word = True


                # delet black_list_word field
                for each_black_list_word in black_lists:
                    is_found_in_key = re.search(each_black_list_word, key)
                    is_found_in_value = re.search(each_black_list_word, value)
                    if(is_found_in_key or is_found_in_value): found_black_list_word = True
                    

                if (value == '' or value == None or value == ' '):                 # delete  field that dont have value
                    found_black_list_word = True

                if( not found_black_list_word):
                    return_str +=  key + ":" + value + "| "

            return_str = re.sub(" *\| *$", '', return_str)
            
            return return_str
    

while True:
    scrape()

