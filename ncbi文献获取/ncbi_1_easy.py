# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:15:58 2017

@author: yjy-006
"""

import urllib
import xlsxwriter as xlsx
import xlrd
from bs4 import BeautifulSoup

url = 'https://www.ncbi.nlm.nih.gov/pubmed/'
info = input('Please input the infomation of Literature:\n')#eg:Reducing Unnecessary Laboratory Testing in the MICU.
post = {'value':str(info)}
postdata = urllib.parse.urlencode(post).encode(encoding =' utf-8')

def info_get(self,url,info,postdata):
    try:
        request = urllib.request.Request(url,data = postdata)
        reponse = urllib.request.urlopen(request) 
        content = reponse.read().decode('utf-8')
        soup = BeautifulSoup(content,'lxml')#eg:28285068
        print('Name: '+ soup.find_all())
        print('\nDetail: '+ soup.fin_all())
        print('\nExcerpt '+ soup.find_all())
        print('\nPMID: '+ soup.find_all())
    except urllib.error.URLError as data:
        print(data)
    name = soup.find_all()
    detail = soup.find_all()
    excerpt = soup.find_all()
    pmid = soup.find_all()
    List = [name,detail,excerpt,pmid]
    return List
    

#建立excel表格，将爬取的数据写入 
def List_read(self,List):
    print('Do you want to create a new file: (send y or n)')
    choice = input('Do you want to create a new file: (send \'y\' to confirm) ')  
    if choice.lower() == 'y':   
        path = input('Please input the path: \n') 
        wb = xlsx.Workbook(str(path))
        ws = wb.add_worksheet('Literature_info')
        items = ['Name','Detail','Author','PMID']
        for i in range(4):
            ws.write(0,i,items[i])
            ws.write(1,i,List[i])
        
    else:
        path = input('Please input the path: \n')
        wb = xlrd.open_workbook(str(path))
        ws = wb.sheet_by_name(ws(0))
        row = input('the num of row:\n')
        for k in range(4):
            ws.write(row,k,List[k])
    ws.close()
        
        

    items = ['Name','Detail','Author','PMID']
    for i in range(4):
        ws.write(0,i,items[i])
        
        
Lit_list = info_get(url,info,postdata)
List_read(Lit_list)