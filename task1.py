# -*- coding: utf-8 -*-
"""
自动获取NCBI文献数据库（PubMed）的文献的软件，指定文献参数，
用Python访问API获取文献ID列表，再通过访问ID对应的文献网页，
用爬虫获取文献信息，整理出报表，报表内容包括（'PMID','Pubdate','Source','Author',
'Title','PubType','FullJournalName','Abstract','ISSN','ImpactFactor'）

@author: khe
"""
from urllib import request
from bs4 import BeautifulSoup
import re
import time
import xlsxwriter as xlsx
import xlrd
import urllib


def sort(keywords):#对输入的相关参数进行整理，避免空格，若出现空格则以+号取代
    para = keywords.split()
    keywords_sorted = ''
    for i in range(len(para)):
        if i == len(para) - 1:
            keywords_sorted = keywords_sorted + para[i]
            break
        keywords_sorted = keywords_sorted + para[i] + '+'
    return keywords_sorted
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
        #新建url连接去爬取文献的摘要信息
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

        
        url1='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=' + str(Id[0])
        #新建url连接去爬去文献对应得ISSN编号信息
        try:
            request1 = urllib.request.Request(url1)
            reponse1 = urllib.request.urlopen(request1)
            content1 = reponse1.read().decode('utf_8')
        except urllib.error.URLError as Error:
            print(Error)
        issn_re = re.compile('<Item Name="ISSN" Type="String">(.*?)</Item>')
        ISSN = str(re.findall(issn_re,content1))
        
        #根据爬取的文献的ISSN信息注释其相应的影响因子信息
        data = xlrd.open_workbook('2013年SCI杂志影响因子列表.xls')
        #读入本地的一个影响因子列表,这个文件就放在python的当前工作目录下
        table = data.sheet_by_index(0)
        nrows = table.nrows
        #如果没有抓到ISSN，则影响因子为空
        print(ISSN)
        ImpactFactor = ''   
        for i in range(nrows):
            cell = '[\'' + table.col(2)[i].value + '\']'
            
            if cell == ISSN:
                ImpactFactor = table.col(4)[i].value
                break
        print(cell)
        print(ImpactFactor)
        list_value = [Id,Pubdate,Source,Author,Title,PubType,FullJournalName,Abstract,ISSN,ImpactFactor]
        return list_value
       
        
    
class Literature:
    #通过相关参数在pubmed中获取相应的文献信息
    def __init__(self,url,search,summary,info_sorted,tool):
        #info_sorted是经过整理得到的相关参数
        #tool网页的正则匹配工具
        #listing建立excel表格，将获取文献信息导入表格
        self.url = url
        self.search = search
        self.summary = summary
        self.info_sorted = info_sorted
        self.tool = tool
        self.Esearch = url + search + str(info_sorted)
        
    def get_uid(self):
        #访问pubmed的API，匹配其中的UID,返回匹配的UID个数
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

class List:
    #创建Excel表格，并导入相关的文献信息
    def create(self,path,Litera,num):
        self.path = path
        self.wb = xlsx.Workbook(str(self.path))
        self.ws = self.wb.add_worksheet('Literature_info')
        list_create = ['PMID','Pubdate','Source','Author',\
                               'Title','PubType','FullJournalName','Abstract','ISSN','ImpactFactor']
        for i in range(len(list_create)):
            self.ws.write(0,i,list_create[i])
        for i in range(num):
            element = Litera.info_ready(i)#网页全部信息
            values = Litera.get_info(element)#通过匹配得到的所需信息
            for k in range(len(values)):#信息顺序录入表格
                
                self.ws.write(i+1,k,str(values[k]))
            print('已成功录入%d条文献信息'%(i+1))
            time.sleep(0.5)
        self.wb.close()
        
        
def main():
      keywords = input('请输入文献搜索的关键词:\n')
      url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
      search = 'esearch.fcgi?db=pubmed&term='
      summary = 'esummary.fcgi?db=pubmed&id='
      path = input('please input the file path:\n')
      listing = List()
      tool = Tool()
      Sorted = sort(keywords)
      Litera = Literature(url,search,summary,Sorted,tool)
      Id_num = Litera.get_uid()
      listing.create(path,Litera,Id_num)
      print('录入完毕\n')
if __name__ == "__main__":
    main() 
      
