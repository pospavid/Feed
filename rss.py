import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from urllib.parse import urljoin
#================================================================
def soup_create(url,site_title,site_description):
    global soup, fg
    # Getting soup of website
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, 'html.parser')
    # Creating the feed
    fg = FeedGenerator()
    fg.title(site_title)
    fg.link(href=url, rel='alternate')
    fg.description(site_description)
    fg.language('cs')
def export_rss(xml_file):
    # Export RSS XML
    global fg
    rss = fg.rss_str(pretty=True)
    with open(xml_file, 'wb') as f:
        f.write(rss)
#===============================================================
# Bydlení Brno
#-------------
soup_create("https://bydleni.brno.cz/aktuality/","Bydlení Brno","RSS feed aktualit z webu bydleni.brno.cz")
# Parsing articles from soup
articles = soup.select('div.col')
for arcticle in articles:
    odkaz = arcticle.find("a")
    title = arcticle.find("small")

    fe = fg.add_entry()
    fe.title(title.text)
    fe.link(href=odkaz["href"])
    fe.description(title.text)
export_rss("bydleni_brno_aktuality.xml")
fg = None
soup = None
#==============================================================
# Brno
#-------------
soup_create("https://cosedeje.brno.cz/rss","Brno","RSS feed aktualit z webu brno.cz")
articles = soup.select('ul li')
for arcticle in articles:
    try:
        odkaz = arcticle.find("a")
        title = odkaz.get_text()

        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=url.replace("rss","")+odkaz["href"])
        fe.description(title)
    except:
        pass
print(fg.rss_str(pretty=True))
export_rss("brno_aktuality.xml")
