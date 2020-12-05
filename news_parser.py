from newspaper import Article
import csv
from normalize_text import normalize_text


class Parser:
    def __init__(self):
        self.allowed_domains = []
        self.sources = {}
        with open('news_ratings.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                key = row[0]
                self.allowed_domains.append(key)
                self.sources[key] = row[1]

    def parse_url(self, url, domain):
        if domain not in self.allowed_domains:
            print(f"{domain} not supported")
            return None
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            data = {"title": normalize_text(article.title),
                    "text": normalize_text(article.text),
                    "source_bias": self.sources[domain]}
            return data
        except:
            return None
