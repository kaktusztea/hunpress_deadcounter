#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

def get_page_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text()

sites = ["https://telex.hu", "https://444.hu", "https://24.hu", "https://hvg.hu", "https://index.hu", \
         "https://www.magyarhirlap.hu", "https://origo.hu", "https://magyarnemzet.hu", "https://hirado.hu"]
words = ["meghal", "halott", "megöl", "áldozat"]

for sitename in sites:
    print("[%s]" % sitename)
    text = get_page_text(sitename)
    for word in words:
        print("%s: %s" % (word, str(text.count(word))))
    print("")