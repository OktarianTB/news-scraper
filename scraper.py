from tld import get_tld
from news_parser import Parser
import requests
from bs4 import BeautifulSoup
import csv


def get_domain_from_url(url):
    try:
        info = get_tld(url, as_object=True)
        return info.domain
    except:
        return None


def scrape_news(topic):
    parser = Parser()
    all_data = []
    sources = ["vox", "cnn", "economist", "cnbc", "foxnews"]

    for source in sources:
        url = f"https://news.google.com/search?q={topic}%20{source}&hl=en-US&gl=US&ceid=US%3Aen"
        try:
            google_news = requests.get(url, timeout=5)
        except:
            return []

        soup = BeautifulSoup(google_news.content, 'html5lib')
        page_links = soup.find_all("a", href=True, class_="VDXfz")

        print(f"Page links for {source} [{topic}]: {len(page_links)}")

        for link in page_links[:500]:
            google_link = f"https://news.google.com{link['href'][1:]}"
            try:
                r = requests.get(google_link, timeout=3)
            except:
                continue

            new_link = r.url

            domain = get_domain_from_url(new_link)
            article_data = parser.parse_url(new_link, domain)
            if article_data:
                new_row = [article_data["title"], article_data["text"], domain, article_data["source_bias"], topic]
                all_data.append(new_row)

    return all_data


#data1 = scrape_news("immigration")
#data3 = scrape_news("trump")
#data4 = scrape_news("vaccine")

data = scrape_news("climate change")

with open(r'news_data.csv', 'a') as f:
    writer = csv.writer(f, lineterminator="\n")
    for row in data:
        try:
            writer.writerow(row)
        except UnicodeEncodeError:
            continue
