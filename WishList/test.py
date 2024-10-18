import datetime
import pandas as pd
import cv2
import numpy as np
import re
import time
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import cv2

def getImage(path):
    response = requests.get(path, allow_redirects=True)
    print(response)
    if response.status_code == 200:
        with open("test.png", 'wb') as f:
            f.write(response.content)
        f.close()
        img = cv2.imread("test.png")
        cv2.imshow("aa",img)
        cv2.waitKey(0)


#amazon scrape
def get_data(pageNo,linkName):  
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    #r = requests.get(linkName+'ref=zg_bs_pg_'+str(pageNo)+'?ie=UTF8&pg='+str(pageNo), headers=headers)#, proxies=proxies)
    r = requests.get(linkName, headers=headers)#, proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content)
    alls = []
    '''
    for d in soup.findAll('div', attrs={'class':'p13n-sc-uncoverable-faceout'}):
        name = d.find('div', attrs={'class':'a-section a-spacing-mini _cDEzb_noop_3Xbw5'})
        price_tag = d.find('div', attrs={'class':'_cDEzb_p13n-sc-price-animation-wrapper_3PzN2'})
        if price_tag is not None:
            price = price_tag.find("span", attrs={'class':'_cDEzb_p13n-sc-price_3mJ9Z'})
            desc = name.find("img")
            print(str(desc['alt'])+"===="+" "+str(desc.get('src'))+str(price.text))
    '''
    for d in soup.findAll('div', attrs={'class':'s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'}):
        name = d.find('img')
        price = d.find("div", attrs={'class':'a-row a-size-base a-color-base'})
        if price is not None:
            price = price.find("span", attrs={'class':'a-price-whole'})
            print(str(name['alt'])+"===="+" "+str(name.get('src'))+" == "+str(price.text))
            getImage(name.get('src'))
    return alls

'''
def get_data(pageNo,linkName):  
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    r = requests.get(linkName, headers=headers)#, proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content)
    alls = []
    for d in soup.findAll('div', attrs={'class':'_2kHMtA'}):
        name = d.find('img')
        price_tag = d.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
        print(str(name['alt'])+"===="+" "+str(name.get('src'))+"==="+str(price_tag.text))
    return alls
'''
url = 'https://www.amazon.in/s?k=redmi'
results = []
results.append(get_data(1,url))
print(results)
'''
url = 'https://www.flipkart.com/search?q=laptop'
results = []
results.append(get_data(1,url))
print(results)
'''
