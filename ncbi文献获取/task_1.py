# -*- coding: utf-8 -*-
"""
将输入的文献相关参数整理规范化，通过NCBI提供的接口找到输入信息的相
关文献ID，并获取。利用文献ID获取相关文献的摘要，并将其中的有关心信
息通过正则匹配得到。根据疾病名称在CDK中找到疾病的同义词信息

@author: ycy
"""

import urllib.request
import urllib
import re
import time
import xlsxwriter as xlsx
import xlrd
from bs4 import BeautifulSoup


class info_sort:
    def sort(self,info):#对输入的相关参数进行整理，避免空格，若出现空格则以+号取代
        para = info.split()
        info_sorted = ''
        for i in range(len(para)):
            if i == len(para) - 1:
                info_sorted = info_sorted + para[i]
                break
            info_sorted = info_sorted + para[i] + '+'
        return info_sorted
            

class Literature:
    #通过相关参数在pubmed中获取相应的文献信息
    def __init__(self,url,search,summary,info_sorted,tool):
        #info_sorted是经过整理得到的相关参数
        #tool网页的正则匹配工具
        #listing建立excel表格，将获取文献信息导入
        self.url = url
        self.search = search
        self.summary = summary
        self.info_sorted = info_sorted
        self.tool = tool
        self.Esearch = url + search +str(info_sorted)
        
    def get_uid(self):
        #访问pubmed的api，匹配其中的UID,返回匹配的UID个数
        try:
            request = urllib.request.Request(self.Esearch)
            reponse = urllib.request.urlopen(request)
            content = reponse.read().decode('utf-8')
        except urllib.error.URLError as Error:
            print(Error)
        patterns = re.compile('<Id>(.*?)</Id>')
        self.Id_s = Id_s = re.findall(patterns,content)
        print('文献ID已成功匹配\n')
        length = len(Id_s)
        return length

    def info_ready(self,i):
        Esummary_b = self.url + self.summary
        Esummary = Esummary_b + str(self.Id_s[int(i)])
        try:
            request = urllib.request.Request(Esummary)
            reponse = urllib.request.urlopen(request)
            content = reponse.read().decode('utf-8')
        except urllib.error.URLError as Error:
            print(Error)
        return content
        
    def get_info(self,element):
        value = self.tool.replace(element)
        return value
        

class Tool:
    #利用正则表达式，匹配文献网页的相关元素
    def __init__(self):
        self.Id_re = re.compile('<Id>(.*?)</Id>')
        self.Pubdate_re = re.compile('<Item Name="PubDate" Type="Date">(.*?)</Item>')
        self.Source_re = re.compile('<Item Name="Source" Type="String">(.*?)</Item>')
        self.Author_re = re.compile('<Item Name="Author" Type="String">(.*?)</Item>')
        self.Title_re = re.compile('<Item Name="Title" Type="String">(.*?)</Item>')
        self.PubType_re = re.compile('<Item Name="PubType" Type="String">(.*?)</Item>')
        self.FullJournalName_re = re.compile('<Item Name="FullJournalName" Type="String">(.*?)</Item>')
        
    def replace(self,content):
        Id = re.findall(self.Id_re,content)
        Pubdate = re.findall(self.Pubdate_re,content)
        Source = re.findall(self.Source_re,content)
        Author = re.findall(self.Author_re,content)
        Title = re.findall(self.Title_re,content)
        PubType = re.findall(self.PubType_re,content)
        FullJournalName = re.findall(self.FullJournalName_re,content)
        url = 'https://www.ncbi.nlm.nih.gov/pubmed/?term=' + str(Id[0])
        try:
            request = urllib.request.Request(url)
            reponse = urllib.request.urlopen(request)
            content = reponse.read().decode('utf-8')
        except urllib.error.URLError as Error:
            print(Error)
        soup = BeautifulSoup(content,'lxml')
        t = soup.find_all('abstracttext')
        pattern = re.compile('<abstract.*?>|</abstracttext>')
        Abstract = re.sub(pattern,'\n',str(t))
        list_value = [Id,Pubdate,Source,Source,Author,Title,PubType,FullJournalName,Abstract]
        return list_value
    
class List:
    #创建Excel表格，并导入相关的文献信息
    def create(self,path,Litera,num):
        self.path = path
        self.wb = xlsx.Workbook(str(self.path))
        self.ws = self.wb.add_worksheet('Literature_info')
        list_create = ['Id','Pubdate','Source','Source','Author',\
                               'Title','PubType','FullJournalName','Abstract']
        for i in range(len(list_create)):
            self.ws.write(0,i,list_create[i])
        for i in range(num):
            element = Litera.info_ready(i)#网页全部信息
            values = Litera.get_info(element)#通过匹配得到的所需信息
            for k in range(len(values)):#信息顺序录入表格
                if k == len(values) - 1:#指定导入abstract信息的条件
                    self.ws.write(i+1,k,str(values[k]))
                else:
                    self.ws.write(i+1,k,str(values[k][0]))
            print('已成功录入%d条文献信息'%(i+1))
            time.sleep(0.5)
        self.wb.close()

class NTB:
    def synonym(self,info):
        url1 = 'http://ctdbase.org/basicQuery.go?bqCat=disease&bq='#CTD疾病库搜索网址
        url2 = 'http://ctdbase.org/detail.go?type=disease&acc='#疾病同义词信息网址
        url = url1 + str(info)
        try:
            request = urllib.request.Request(url)
            reponse = urllib.request.urlopen(request)
            content = reponse.read().decode('utf-8')
        except urllib.error.URLError as Error:
            print(Error)
        soup = BeautifulSoup(content,'lxml')
        t = soup.find_all('span',class_="match")
        pattern1 = re.compile('<a href=.*?>(.*?)</a>')#匹配多行信息中的名字的模式
        pattern2 = re.compile('<a href="(.*?)">.*?</a>')#匹配相应的网址的模式
        pattern3 = re.compile('/detail.go.*?acc=(.*)')#匹配网址信息的acc部分的模式
        name = re.findall(pattern1,str(t))
        url = re.findall(pattern2,str(t))
        for i in range(len(name)):
            if name[i] == info:
                acc = re.findall(pattern3,str(url[i]))
                break;
        url_s = url2 + str(acc[0])
        
        try:
            request = urllib.request.Request(url_s)
            reponse = urllib.request.urlopen(request)
            content = reponse.read().decode('utf-8')
        except urllib.error.URLError as Error:
            print(Error)
        pattern4 = re.compile('<a href=".*?" title="Keyword query" rel="nofollow">(.*?)</a>')
        return re.findall(pattern4,content)

#def filters(synonyms,):#之后需要对NTB的函数进行更改
    #for i in range(len(synonym)):
        
    

def MainLoop():
    info =input('请输入基因名称;\n')
    sorting = info_sort()
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    search = 'esearch.fcgi?db=pubmed&term='
    summary = 'esummary.fcgi?db=pubmed&id='
    path = input('input the file path:\n')
    listing = List() 
    tool = Tool() 
    Litera = Literature(url,search,summary,sorting.sort(info),tool)
    Id_num = Litera.get_uid()
    ntb = NTB()
    synonyms = ntb.synonym(info)
    print(synonyms)
    listing.create(path,Litera,Id_num)


mainloop = MainLoop()


                   


