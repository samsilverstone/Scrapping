# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 23:59:02 2019

@author: Sam Silverstone
"""

import requests,bs4,openpyxl
from fake_useragent import UserAgent
import time
ua=UserAgent()
proxy2=[]
#-----------------------getting proxies----------------------------->
def getproxy():
    scrap=requests.get("https://www.sslproxies.org/")
    soup=bs4.BeautifulSoup(scrap.text,'html.parser')
    x=soup.find(id="proxylisttable")
    count=0
    proxy=[]
    
    for tr in x.tbody:
        for td in tr:
            count+=1
            proxy.append(td.getText())
            if count==2:
                proxy2.append({'ip'     :   proxy[0],
                               'port'  :   proxy[1]})
                count=0
                del proxy[0],proxy[0]
                break
            
def oneproxypls():
    x=proxy2.pop(0)
    return {'http ': 'http://{}:{}'.format(x['ip'],x['port']),
            'no_proxy': 'None'}
        
#------------------------------------------------------------------------------>
def main():
    wb=openpyxl.load_workbook('data.xlsx')
    mb=openpyxl.Workbook()
    sheet2=mb.active
    sheet=wb.active
    list1=[]
    header=['tconst','averageRating','numVotes','movieName']
    max_row=sheet.max_row
    max_column=sheet.max_column
    first_row=int(input("Enter the first row:\n"))
    last_row=int(input("Enter the second row:\n"))
    diff=last_row-first_row  
    #-------------------------titles------------------>
    
    
    for i in range(1,len(header)+1):
        sheet2.cell(row=1,column=i).value=header[i-1]
        
        
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX>
#-------------------------Value-Picking------------------>


    for j in range(1,4):    
        for i in range(2,diff+3):
            sheet2.cell(row=i,column=j).value=sheet.cell(row=(first_row-2)+i,column=j).value
            print(sheet2.cell(row=i,column=j).value)

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX>
        
#---------------------------Scraping data from the site---------------------->
    getproxy()
    pro=oneproxypls()
    headers={'User-Agent':ua.random} 
    for i in sheet2.iter_cols(min_row=2,max_row=diff+2,min_col=1,max_col=1):
        for j in i:
            try:
                print("getting address")
                req=requests.get("https://www.imdb.com/title/"+str(j.value),proxies=pro,headers=headers)
                soup=bs4.BeautifulSoup(req.text,'html.parser')
                x=soup.find('div',class_="title_wrapper")
                list1.append(x.h1.getText())
                print(list1)
            except:
                print("Proxy {} not working, changing it".format(pro))
                pro=oneproxypls()

                headers={'User-Agent':ua.random} 
            else:
                print("Written in the {} successfully".format(j.value))    
            
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX>

    for i in range(2,diff+3):
        sheet2.cell(row=i,column=4).value=list1[i-2]
        print("Inserting value:{}".format(list1[i-2]))      
    print(list1)
    mb.save("newworld.xlsx")

if __name__=="__main__":
    main()        
#XXXXXXXXXXXXXXXXXXXXXXPicking values from rottentomatoesXXXXXXXXXXXXXXXXXXXX>
    proxies = {
            'http' :'http://91.211.122.23:33872',
            'no_proxy':'None'
            }
    print(proxies)
    req=requests.get("https://www.rottentomatoes.com/m/uri",proxies=proxies)
    
    req.request.headers


    soup=bs4.BeautifulSoup(req.text,'html.parser')
    x=soup.find('span',class_="mop-ratings-wrap__percentage").getText()
    y=soup.find('span',class_="mop-ratings-wrap__percentage mop-ratings-wrap__percentage--audience").getText()
    print(y.strip()[:4])
    print(x.strip())
        
    
