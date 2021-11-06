#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import os
import sys
import time
import signal
import requests
import sqlite3
import datetime


from enum import IntEnum
class Detailed(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


def get_page_text(url):
    try:
        r = requests.get(url, verify=True, timeout=5)
    except requests.exceptions.ConnectionError:
        print("Request rejected. Skipping.")
        return False
    except requests.exceptions.ReadTimeout:
        print("No response from host [%s]. Skipping." % url)
        return False
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text()


def sql_init():
    connection = None
    dbfile = "stats.db"
    if not os.path.isfile(dbfile):
        connection = sql_connection(dbfile)
        sql_table_init(connection)
    else:
        connection = sql_connection(dbfile)
    return connection


def sql_connection(dbfile):
    try:
        conn = sqlite3.connect(dbfile)
        return conn
    except Exception as Error:
        print("[ERROR] Database connection failed. %s" % Error)
        sys.exit(1)


def sql_table_init(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE stats(id integer PRIMARY KEY AUTOINCREMENT,  \
                                    date TIMESTAMP NOT NULL, \
                                    sitename TEXT NOT NULL,  \
                                    word TEXT NOT NULL,       \
                                    count INTEGER);")
    con.commit()


def sql_store(date, sitename, word, count):
    if not connection:
        print("[ERROR] No database connection. Exiting...")
        sys.exit(1)
    cr = connection.cursor()

    data_tuple = (date, sitename, word, count)
    sqlite_insert_with_param = "INSERT INTO 'stats' ('date', 'sitename', 'word', 'count') VALUES (?, ?, ?, ?);"
    try:
        cr.execute(sqlite_insert_with_param, data_tuple)
        connection.commit()
    except sqlite3.Error as err:
        print("[SQLERROR] Failed INSERT operation. %s" % err)
        connection.close()
        sys.exit(1)


def poll_sites(sites, words):
    # Iterate on sites, get their HTML content, create statistics
    for sitename in sites:
        summa = 0
        if detailed >= Detailed.MEDIUM:
            print("\n[%s]" % sitename)
        text = get_page_text(sitename)
        if not text:
            continue
        dt = datetime.datetime.now()
        for key in words.keys():
            ct = bct = 0
            ct = text.lower().count(key)
            for bword in words[key]:
                bct += text.lower().count(bword)
            nct = (ct - bct)
            summa += nct
            if detailed == Detailed.HIGH:
                print("%s: %s" % (key, str(nct)))
            if sql:
                sql_store(dt, sitename, key, nct)
        if detailed >= Detailed.MEDIUM:
            print("(%s)" % str(summa))
        if sql:
            sql_store(dt, sitename, "sum", summa)


def ctrlc_handler(signum, frame):
    print("\nPolling ended. Exiting.")
    if sql:
        connection.close()
        if debug:
            print("[DEBUG] SQLite connection closed.")
    sys.exit(1)


def main():
    global connection, detailed, debug, sql    # SQLite connection, detailed mode, debug mode, SQLite storing
    period = 1                                 # polling period in minutes
    iteration = 1                              # counter for polling loop
    detailed = Detailed.HIGH
    debug = True
    sql = True

    if sql:
        connection = sql_init()
        if connection and debug:
            print("[DEBUG] SQLite connection opened.")
        elif not connection:
            print("[ERROR] No SQLite connection.")
            sys.exit(1)

    # Observered websites
    sites = ["https://telex.hu", "https://444.hu", "https://24.hu", "https://hvg.hu", "https://index.hu",      \
            "https://www.magyarhirlap.hu", "https://origo.hu", "https://magyarnemzet.hu", "https://hirado.hu", \
            "https://tenyek.hu", "https://blikk.hu"]

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

    signal.signal(signal.SIGINT, ctrlc_handler)
    
    print("\nPolling starts, interval: %d minute(s)." % period)
    print("Stop by pressing CTRL+C.\n")
    while True:                                          # endless loop, break by CTRL+C
        print("#%s." % str(iteration))
        poll_sites(sites, words)
        if debug:
            print("\n[DEBUG] Sleeping %d seconds.\n" % 60 * period)
        time.sleep(60 * period)
        iteration += 1
    
if __name__ == "__main__":
    main()