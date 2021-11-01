#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests


def get_page_text(url):
    try:
        r = requests.get(url, verify=True, timeout=5)
    except requests.exceptions.ConnectionError:
        print("Request rejected. Skipping.")
        return False
    except requests.exceptions.ReadTimeout:
        print("No response from host. Skipping.")
        return False
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text()


if __name__ == "__main__":

    # Observered websites
    sites = ["https://telex.hu", "https://444.hu", "https://24.hu", "https://hvg.hu", "https://index.hu", \
            "https://www.magyarhirlap.hu", "https://origo.hu", "https://magyarnemzet.hu", "https://hirado.hu"]

    # Searched keywords and their blacklisted exception phrases
    words = {
                 "meghal": ["meghall", "meghalad"],
                 "halott": ["halottak napj", "halottaskocsi", "halottkém", "halottnak a csók", "halottkultusz"],
                 "megöl": ["megölel"],
                 "áldozat": ["áldozati póz"],
                 "agyonvert": [],
                 "meggyilkol": [],
                 "gyilkos": ["gyilkos tréfa"]
                }

    # Iterate on sites, get their HTML content, create statistics
    for sitename in sites:
        summa = 0
        bsumma = 0
        print("\n[%s]" % sitename)
        text = get_page_text(sitename)
        if not text:
            continue
        for key in words.keys():
            ct = bct = 0
            ct = text.lower().count(key)
            for bword in words[key]:
                bct += text.lower().count(bword)
            summa += (ct - bct)
            print("%s: %s" % (key, str(ct - bct)))
        print("(%s)" % str(summa))