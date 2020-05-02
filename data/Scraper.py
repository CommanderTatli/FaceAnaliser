import time
import urllib3
from bs4 import BeautifulSoup
import requests
import re
from html.parser import HTMLParser
import urllib.request
import pickle

found = []
between = ""


class TD_finder(HTMLParser):
    def handle_endtag(self, tag):
        global found, between
        if tag == "td":
            found.append(between)

    def handle_data(self, data):
        global between
        between = data


def get_all_urls():
    site = requests.get("https://www.nndb.com/")
    tries = 5
    while site.status_code != requests.codes.ok and tries:
        tries -= 1
        site = requests.get("https://www.nndb.com/")
    if site.status_code != requests.codes.ok:
        raise ConnectionError("Site is unreachable!")
    lists = re.findall('http://www.nndb.com/lists/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                       str(site.content))[:26]

    urls = []
    for list in lists:
        urls += get_urls(list)
        time.sleep(5)

    return urls


def get_urls(url):
    global found
    urls = []
    site = requests.get(url)
    tries = 5
    while site.status_code != requests.codes.ok and tries:
        time.sleep(5)
        tries -= 1
        site = requests.get(url)
    if site.status_code == requests.codes.ok:
        html = str(site.content)
        td = TD_finder()
        td.feed(html)
        found = found[6:-4]
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')

        counter = 0
        for i in links:
            try:
                if "people" in i['href']:
                    if (found[4 + counter * 5] == "-" or int(found[4 + counter * 5][-4:]) > 1920):
                        urls.append(i['href'])
                    counter += 1
            except ValueError:
                counter += 1

    return urls


def find_in_text(regex, text):
    x = re.search(regex, text)
    if x is None:
        return "None"
    else:
        return x.group(1)


def scrape(url):
    time.sleep(10)
    site = requests.get(url)
    tries = 5
    while site.status_code != requests.codes.ok and tries:
        time.sleep(5)
        tries -= 1
        site = requests.get(url)
    if site.status_code != requests.codes.ok:
        raise ConnectionRefusedError("No connection.")
    text = re.sub(re.compile('<.*?>'), '', str(site.content))

    name = find_in_text("<b>([A-Za-z ]*)</b>+</font>", str(site.content))
    gender = find_in_text("Gender: ([A-Z][a-z]*)", text)
    religion = find_in_text("Religion: ([A-Z][a-z]*)", text)
    race = find_in_text("Race or Ethnicity: ([A-Z][a-z]*)", text)
    orientation = find_in_text("Sexual orientation: ([A-Z][a-z]*)", text)
    occupation = find_in_text("Occupation: ([A-Z][a-z]*)", text)
    children = text.count("Son") + text.count("Daughter")
    siblings = text.count("Brother") + text.count("Sister")
    spauses = text.count("Wife") + text.count("Husband")
    obesity = "Obesity" in text
    alcoholism = "Alcoholism" in text
    marijuana = "Marijuana" in text

    pic_name = re.search("<p>+<img src=\"([A-Za-z0-9-]*)\\.(gif|jpg|png|jpeg)", str(site.content))
    pic_url = "None"
    if pic_name is not None:
        pic_url = pic_name.group(1) + "." + pic_name.group(2)
        urllib.request.urlretrieve(url + pic_url, "pictures/" + pic_url)

    return {"name": name, "gender": gender, "religion": religion, "race": race, "orientation": orientation,
            "occupation": occupation, "pic": pic_url, "children": children, "spauses": spauses, "siblings": siblings,
            "obesity": obesity, "alcoholism": alcoholism, "marijuana": marijuana}


# urls = get_urls("https://www.nndb.com/lists/518/000063329/")
urls = get_all_urls()
data = []
print(len(urls), " records to scrape")
for i in range(len(urls)):
    try:
        data.append(scrape(urls[i]))
    except ConnectionResetError or OSError or urllib3.exceptions.NewConnectionError or \
           urllib3.exceptions.MaxRetryError or requests.exceptions.ConnectionError:
        print("Connection error occured. Waiting...")
        for i in range(100):
            print(100 - i, "s left...")
            time.sleep(1)
            i -= 1
    print(i + 1, " profiles scraped!")

# data.append(scrape("https://www.nndb.com/people/430/000043301/"))
# print("scraped!")
with open('data.txt', 'a') as file:
    for record in data:
        text = ""
        for attr in record.keys():
            text += (attr + ":" + str(record[attr]) + ";")
        text = text[:-1] + "\n"
        file.write(text)
