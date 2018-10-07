from bs4 import BeautifulSoup
import urllib.request

import logging
logging.basicConfig(filename='scraper.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info("\n\n\nStarting\n\n\n")
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

page = "https://en.wikipedia.org/wiki/Morgan_Freeman"
with urllib.request.urlopen(page) as url:
    html = url.read()
soup = BeautifulSoup(html, 'lxml')
print(soup.prettify())
