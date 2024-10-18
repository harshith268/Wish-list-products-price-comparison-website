from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import os

img_index = 0

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})   

def Aboutus(request):
    if request.method == 'GET':
       return render(request, 'Aboutus.html', {})
    
def SearchProduct(request):
    if request.method == 'GET':
       return render(request, 'SearchProduct.html', {})

def getImage(path):
    global img_index
    response = requests.get(path, allow_redirects=True)
    flag = False
    if response.status_code == 200:
        with open("WishListApp/static/products/"+str(img_index)+".png", 'wb') as f:
            f.write(response.content)          
        f.close()
        flag = True

def amazonScrape(path):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    r = requests.get(path, headers=headers)
    content = r.content
    soup = BeautifulSoup(content)
    product = []
    prices = []
    image = []
    for d in soup.findAll('div', attrs={'class':'s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'}):
        name = d.find('img')
        price = d.find("div", attrs={'class':'a-row a-size-base a-color-base'})
        if price is not None:
            price = price.find("span", attrs={'class':'a-price-whole'})
            prices.append(price.text)
            product.append(name['alt'])
            image.append(name.get('src'))
    return product, image, prices

def FlipkartScrape(path):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    r = requests.get(path, headers=headers)#, proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content)
    product = []
    prices = []
    image = []
    for d in soup.findAll('div', attrs={'class':'_2kHMtA'}):
        name = d.find('img')
        price_tag = d.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
        prices.append(price_tag.text)
        product.append(name['alt'])
        image.append(name.get('src'))
    return product, image, prices
            
def SearchProductAction(request):
    if request.method == 'POST':
        global img_index
        for root, dirs, directory in os.walk("E:/venkat/2021/December22/WishList/WishListApp/static/products"):
            for j in range(len(directory)):
                if os.path.exists("E:/venkat/2021/December22/WishList/WishListApp/static/products/"+directory[j]):
                    os.remove("E:/venkat/2021/December22/WishList/WishListApp/static/products/"+directory[j])
        query = request.POST.get('t1', False)
        output = '<table border="1" align="center">'
        output+='<tr><th><font size="" color="black">Ecommerce Site</th><th><font size="" color="black">Product Description</th><th><font size="" color="black">Image</th><th><font size="" color="black">Price</th><th><font size="" color="black">Visit Website</th></tr>'
        product, image, prices = amazonScrape("https://www.amazon.in/s?k="+query)
        qry = "https://www.amazon.in/s?k="+query
        for i in range(len(product)):
            getImage(image[i])
            output+='<tr><td><font size="" color="black">Amazon</td><td><font size="" color="black">'+product[i]+'</td>'
            output+='<td><img src="/static/products/'+str(img_index)+'.png" width="200" height="200"></img></td>'
            output+='<td><font size="" color="black">'+prices[i]+'</td>'
            output+='<td><a href='+qry+' target="_blank"><font size=3 color=black>Click Here to Visit Website</font></a></td></tr>'
            img_index = img_index + 1  
        product, image, prices = FlipkartScrape("https://www.flipkart.com/search?q="+query)
        qry = "https://www.flipkart.com/search?q="+query
        for i in range(len(product)):
            getImage(image[i])
            output+='<tr><td><font size="" color="black">Flipkart</td><td><font size="" color="black">'+product[i]+'</td>'
            output+='<td><img src="/static/products/'+str(img_index)+'.png" width="200" height="200"></img></td>'
            output+='<td><font size="" color="black">'+prices[i]+'</td>'
            output+='<td><a href='+qry+' target="_blank"><font size=3 color=black>Click Here to Visit Website</font></a></td></tr>'
            img_index = img_index + 1  
        context= {'data':output}
        return render(request, 'ViewResult.html', context)                    
            
            
  
    
def Signup(request):
    if request.method == 'POST':
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      contact = request.POST.get('contact', False)
      email = request.POST.get('email', False)
      address = request.POST.get('address', False)
      utype = request.POST.get('type', False)
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'WishList',charset='utf8')
      db_cursor = db_connection.cursor()
      student_sql_query = "INSERT INTO register(username,password,contact,email,address,usertype) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"','"+utype+"')"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      if db_cursor.rowcount == 1:
       context= {'data':'Signup Process Completed'}
       return render(request, 'Register.html', context)
      else:
       context= {'data':'Error in signup process'}
       return render(request, 'Register.html', context)    
        
def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        utype = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'WishList',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    utype = row[5]
                    break
        if utype == 'User':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        if utype == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)        
        
        
