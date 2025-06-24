import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin

url = 'https://bydleni.brno.cz/aktuality/'
resp = requests.get(url)
resp.raise_for_status()
soup = BeautifulSoup(resp.content, 'html.parser')

fg = FeedGenerator()
fg.title('Aktuality z Bydleni Brno')
fg.link(href=url, rel='alternate')
fg.description('Automaticky generovaný RSS feed – nejnovější články')
fg.language('cs')

# Hledáme všechny články podle <div class="col">
articles = soup.select('div.col')
for arcticle in articles:
    odkaz = arcticle.find("a")
    title = arcticle.find("small")
    print(title.text)
    print(odkaz["href"])

    fe = fg.add_entry()
    fe.title(title.tetx)
    fe.link(href=odkaz["href"])
    fe.description(title.text)

rss = fg.rss_str(pretty=True)
with open('bydleni_brno_aktuality.xml', 'wb') as f:
    f.write(rss)
print("RSS feed vytvořen: bydleni_brno_aktuality.xml")
