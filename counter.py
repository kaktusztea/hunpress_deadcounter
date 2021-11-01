#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

def get_page_text(url):
    try:
        r = requests.get(url, verify=True, timeout=5)
    except requests.exceptions.ConnectionError:
        print("Request rejected. Skipping.")
        return "False"
    except requests.exceptions.ReadTimeout:
        print("No response from host. Skipping.")
        return "False"
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text()

sites = ["https://telex.hu", "https://444.hu", "https://24.hu", "https://hvg.hu", "https://index.hu", \
         "https://www.magyarhirlap.hu", "https://origo.hu", "https://magyarnemzet.hu", "https://hirado.hu"]
words = ["meghal", "halott", "megöl", "áldozat"]

for sitename in sites:
    summa = 0
    print("[%s]" % sitename)
    text = get_page_text(sitename)
    if text == "False":
        print("")
        continue
    for word in words:
        ct = text.count(word)
        summa += ct
        print("%s: %s" % (word, str(ct)))
    print("(%s)\n" % str(summa))