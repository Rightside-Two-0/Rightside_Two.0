#!/usr/bin/env python3
from bs4 import BeautifulSoup
import urllib2

page = urllib2.urlopen('https://www.crexi.com/properties/317972/minnesota-241-w-lake-ave').read()
soup = BeautifulSoup(page)
soup.prettify()
for anchor in soup.findAll('a', href=True):
    print(anchor['href'])
