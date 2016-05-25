# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup

import re
import os

strx = 'query spring 2 3  4 /4 5'
pages = re.findall(r'(.*) /(\d+ *)$', strx)
if pages:
    page = pages.pop()
    print(page[0])
    print(page[1])
else:
    print(strx.strip())
# bs = BeautifulSoup(open('D:/test.html'))

# for el in bs.select('#maincontent > .im'):
#     if el.a != None:
#         uri = el.a['href'];
#         ico = el.a.img['src']
#         print(os.path.basename(ico))
#         header = el.select('.im-header')[0]
#         desc = el.select('.im-description')[0].get_text().strip()
#         order = header.select('.im-title > span')[0].get_text().strip()
#         title = header.select('.im-title > a')[0].get_text().strip()
#         subtitle1 = header.select('.im-subtitle > a')[0].get_text().strip()
#         subtitle2 = header.select('.im-subtitle > a')[1].get_text().strip()
#
