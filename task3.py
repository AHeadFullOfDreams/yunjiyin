# -*- coding: utf-8 -*-
"""
处理从NCBI文献数据库（PubMed）上获取的以关键词：insect+transcriptome所爬取的
2203条文献信息，内容包括（'PMID','Pubdate','Source','Author',
'Title','PubType','FullJournalName','Abstract'）
文献数据分析目的：
1.按年份，按大的昆虫分类，把爬取下来的昆虫转录组文章分别统计数目
2.从标题或摘要里面提取evolution,phylogen(不完全匹配)等关键字，看看进化
  相关研究的昆虫转录组文章有多少，同样按年份、昆虫分类进行文章数目的统计
3.NCBI上检索昆虫转录组，按年统计：昆虫的目、种的增长曲线，2014年应该在目级别
  有一个巨大的增长（Misof et al.2014,所有的昆虫目，100种左右的种），2017年
  应该在种级别有一个巨大增长（Peters et al., 200种左右的蜂类）

@author: khe
"""
import re
import numpy as np
import matplotlib.pyplot as plt
def draw_bar(labels,quants,xlable,ylable,title,aa,i):
      #画柱状图
      width = 0.2  
      ind = np.linspace(0.5,9.5,aa)  
      # make a square figure  
      fig = plt.figure(i)  
      ax  = fig.add_subplot(111)  
      # Bar Plot  
      ax.bar(ind-width/2,quants,width,color='green')  
      # Set the ticks on x-axis  
      ax.set_xticks(ind)  
      ax.set_xticklabels(labels)  
      # labels  
      ax.set_xlabel(xlable)  
      ax.set_ylabel(ylable)  
      # title  
      ax.set_title(title, bbox={'facecolor':'0.8', 'pad':5})  
      plt.grid(True)  
      plt.show()  
      


class Statistics():
      #初始化变量为零，循环句柄文件进行正则匹配，计数
      yearof2017 = 0
      yearof2016 = 0
      yearof2015 = 0
      yearof2014 = 0
      yearof2013 = 0
      yearof2012 = 0
      yearof2011 = 0
      yearof2010 = 0
      yearof2009 = 0
      yearof2008 = 0
      yearof2007 = 0
      yearof2006 = 0
      yearof2005 = 0
      yearof2004 = 0
      yearof2003 = 0
      yearof2002 = 0
      yearof2001 = 0
      yearof2000 = 0
      yearof1999 = 0
      numberofArchaeognatha = 0
      numberofBlattodea = 0
      numberofColeoptera = 0
      numberofDermaptera = 0
      numberofDiptera = 0
      numberofEmbioptera = 0
      numberofEphemeroptera = 0
      numberofGrylloblattodea = 0
      numberofHemiptera = 0
      numberofHymenoptera = 0
      numberofIsoptera = 0
      numberofLepidoptera = 0
      numberofMantodea = 0
      numberofMantophasmatodea = 0
      numberofMecoptera = 0
      numberofMegaloptera = 0
      numberofNeuroptera = 0
      numberofOdonata = 0
      numberofOrthoptera = 0
      numberofPhasmatodea = 0
      numberofPhthiraptera = 0
      numberofPlecoptera = 0
      numberofPsocoptera = 0
      numberofRaphidioptera = 0
      numberofSiphonaptera = 0
      numberofStrepsiptera = 0
      numberofThysanoptera = 0
      numberofTrichoptera = 0
      numberofZoraptera = 0
      #初始化正则表达式
      rgx1 = re.compile(".*?\['2017.*?")
      rgx2 = re.compile(".*?\['2016.*?")
      rgx3 = re.compile(".*?\['2015.*?")
      rgx4 = re.compile(".*?\['2014.*?")
      rgx5 = re.compile(".*?\['2013.*?")
      rgx6 = re.compile(".*?\['2012.*?")
      rgx7 = re.compile(".*?\['2011.*?")
      rgx8 = re.compile(".*?\['2010.*?")
      rgx9 = re.compile(".*?\['2009.*?")
      rgx10 = re.compile(".*?\['2008.*?")
      rgx11 = re.compile(".*?\['2007.*?")
      rgx12 = re.compile(".*?\['2006.*?")
      rgx13 = re.compile(".*?\['2005.*?")
      rgx14 = re.compile(".*?\['2004.*?")
      rgx15 = re.compile(".*?\['2003.*?")
      rgx16 = re.compile(".*?\['2002.*?")
      rgx17 = re.compile(".*?\['2001.*?")
      rgx18 = re.compile(".*?\['2000.*?")
      rgx19 = re.compile(".*?\['1999.*?")
      rgx20 = re.compile(".*?Archaeognatha.*?")
      rgx21 = re.compile(".*?Blattodea.*?")
      rgx22 = re.compile(".*?Coleoptera.*?")
      rgx23 = re.compile(".*?Diptera.*?")
      rgx24 = re.compile(".*?Embioptera.*?")
      rgx25 = re.compile(".*?Ephemeroptera.*?")
      rgx26 = re.compile(".*?Grylloblattodea.*?")
      rgx27 = re.compile(".*?Hemiptera.*?")
      rgx28 = re.compile(".*?Hymenoptera.*?")
      rgx29 = re.compile(".*?Isoptera.*?")
      rgx30 = re.compile(".*?Lepidoptera.*?")
      rgx31 = re.compile(".*?Mantodea.*?")
      rgx32 = re.compile(".*?Mantophasmatodea.*?")
      rgx33 = re.compile(".*?Mecoptera.*?")
      rgx34 = re.compile(".*?Megaloptera.*?")
      rgx35 = re.compile(".*?Neuroptera.*?")
      rgx36 = re.compile(".*?Odonata.*?")
      rgx37 = re.compile(".*?Orthoptera.*?")
      rgx38 = re.compile(".*?Phasmatodea.*?")
      rgx39 = re.compile(".*?Phthiraptera.*?")
      rgx40 = re.compile(".*?Plecoptera.*?")
      rgx41 = re.compile(".*?Psocoptera.*?")
      rgx42 = re.compile(".*?Raphidioptera.*?")
      rgx43 = re.compile(".*?Siphonaptera.*?")
      rgx44 = re.compile(".*?Strepsiptera.*?")
      rgx45 = re.compile(".*?Thysanoptera.*?")
      rgx46 = re.compile(".*?Trichoptera.*?")
      rgx47 = re.compile(".*?Zoraptera.*?")

      def __init__(self,file):
            self.lines = file
      def year(self):
            
            line = self.lines.readline()
            for i in range(8659):
                  
                  if re.search(self.rgx1,line):
                        self.yearof2017 = self.yearof2017 + 1
                  elif re.search(self.rgx2,line):
                        self.yearof2016 = self.yearof2016 + 1
                  elif re.search(self.rgx3,line):
                        self.yearof2015 = self.yearof2015 + 1
                  elif re.search(self.rgx4,line):
                        self.yearof2014 = self.yearof2014 + 1
                  elif re.search(self.rgx5,line):
                        self.yearof2013 = self.yearof2013 + 1
                  elif re.search(self.rgx6,line):
                        self.yearof2012 = self.yearof2012 + 1
                  elif re.search(self.rgx7,line):
                        self.yearof2011 = self.yearof2011 + 1
                  elif re.search(self.rgx8,line):
                        self.yearof2010 = self.yearof2010 + 1
                  elif re.search(self.rgx9,line):
                        self.yearof2009 = self.yearof2009 + 1
                  elif re.search(self.rgx10,line):
                        self.yearof2008 = self.yearof2008 + 1
                  elif re.search(self.rgx11,line):
                        self.yearof2007 = self.yearof2007 + 1
                  elif re.search(self.rgx12,line):
                        self.yearof2006 = self.yearof2006 + 1
                  elif re.search(self.rgx13,line):
                        self.yearof2005 = self.yearof2005 + 1
                  elif re.search(self.rgx14,line):
                        self.yearof2004 = self.yearof2004 + 1
                  elif re.search(self.rgx15,line):
                        self.yearof2003 = self.yearof2003 + 1
                  elif re.search(self.rgx16,line):
                        self.yearof2002 = self.yearof2002 + 1
                  elif re.search(self.rgx17,line):
                        self.yearof2001 = self.yearof2001 + 1
                  elif re.search(self.rgx18,line):
                        self.yearof2000 = self.yearof2000 + 1
                  elif re.search(self.rgx19,line):
                        self.yearof1999 = self.yearof1999 + 1

                  line = self.lines.readline()
                  
            return [self.yearof2017,self.yearof2016,self.yearof2015,self.yearof2014,self.yearof2013,self.yearof2012,self.yearof2011,self.yearof2010,self.yearof2009,self.yearof2008,self.yearof2007,self.yearof2006,self.yearof2005,self.yearof2004,self.yearof2003,self.yearof2002,self.yearof2001,self.yearof2000,self.yearof1999]
      def taxonomy(self):

            line = self.lines.readline()
            for i in range(8659):
                  
            
                  if re.search(self.rgx20,line):
                        self.numberofArchaeognatha = self.numberofArchaeognatha + 1
                  elif re.search(self.rgx21,line):
                        self.numberofBlattodea = self.numberofBlattodea + 1
                  elif re.search(self.rgx21,line):
                        self.numberofColeoptera = self.numberofColeoptera + 1
                  elif re.search(self.rgx22,line):
                        self.numberofDermaptera = self.numberofDermaptera + 1
                  elif re.search(self.rgx23,line):
                        self.numberofDiptera = self.numberofDiptera + 1
                  elif re.search(self.rgx24,line):
                        self.numberofEmbioptera = self.numberofEmbioptera + 1
                  elif re.search(self.rgx25,line):
                        self.numberofEphemeroptera = self.numberofEphemeroptera + 1
                  elif re.search(self.rgx26,line):
                        self.numberofGrylloblattodea = self.numberofGrylloblattodea + 1
                  elif re.search(self.rgx27,line):
                        self.numberofHemiptera = self.numberofHemiptera + 1
                  elif re.search(self.rgx28,line):
                        self.numberofHymenoptera = self.numberofHymenoptera + 1
                  elif re.search(self.rgx29,line):
                        self.numberofIsoptera = self.numberofIsoptera + 1
                  elif re.search(self.rgx30,line):
                        self.numberofLepidoptera = self.numberofLepidoptera + 1
                  elif re.search(self.rgx31,line):
                        self.numberofMantodea = self.numberofMantodea + 1
                  elif re.search(self.rgx32,line):
                        self.numberofMantophasmatodea = self.numberofMantophasmatodea + 1
                  elif re.search(self.rgx33,line):
                        self.numberofMecoptera = self.numberofMecoptera + 1
                  elif re.search(self.rgx34,line):
                        self.numberofMegaloptera = self.numberofMegaloptera + 1
                  elif re.search(self.rgx35,line):
                        self.numberofNeuroptera = self.numberofNeuroptera + 1
                  elif re.search(self.rgx36,line):
                        self.numberofOdonata = self.numberofOdonata + 1
                  elif re.search(self.rgx37,line):
                        self.numberofOrthoptera = self.numberofOrthoptera + 1
                  elif re.search(self.rgx38,line):
                        self.numberofPhasmatodea = self.numberofPhasmatodea + 1
                  elif re.search(self.rgx39,line):
                        self.numberofPhthiraptera = self.numberofPhthiraptera + 1
                  elif re.search(self.rgx40,line):
                        self.numberofPlecoptera = self.numberofPlecoptera + 1
                  elif re.search(self.rgx41,line):
                        self.numberofPsocoptera = self.numberofPsocoptera + 1
                  elif re.search(self.rgx42,line):
                        self.numberofRaphidioptera = self.numberofRaphidioptera + 1
                  elif re.search(self.rgx43,line):
                        self.numberofSiphonaptera = self.numberofSiphonaptera + 1
                  elif re.search(self.rgx44,line):
                        self.numberofStrepsiptera = self.numberofStrepsiptera + 1
                  elif re.search(self.rgx45,line):
                        self.numberofThysanoptera = self.numberofThysanoptera + 1
                  elif re.search(self.rgx46,line):
                        self.numberofTrichoptera = self.numberofTrichoptera + 1
                  elif re.search(self.rgx47,line):
                        self.numberofZoraptera = self.numberofZoraptera + 1
                  line = self.lines.readline()
                  
            print(self.numberofArchaeognatha,self.numberofBlattodea,self.numberofColeoptera,self.numberofDermaptera,self.numberofDiptera,self.numberofEmbioptera,self.numberofEphemeroptera,self.numberofGrylloblattodea,self.numberofHemiptera,self.numberofHymenoptera,self.numberofIsoptera,self.numberofLepidoptera,self.numberofMantodea,self.numberofMantophasmatodea,self.numberofMecoptera,self.numberofMegaloptera,self.numberofNeuroptera,self.numberofOdonata,self.numberofOrthoptera,self.numberofPhasmatodea,self.numberofPhthiraptera,self.numberofPlecoptera,self.numberofPsocoptera,self.numberofRaphidioptera,self.numberofSiphonaptera,self.numberofStrepsiptera,self.numberofThysanoptera,self.numberofTrichoptera,self.numberofZoraptera)      
            return [self.numberofArchaeognatha,self.numberofBlattodea,self.numberofColeoptera,self.numberofDermaptera,self.numberofDiptera,self.numberofEmbioptera,self.numberofEphemeroptera,self.numberofGrylloblattodea,self.numberofHemiptera,self.numberofHymenoptera,self.numberofIsoptera,self.numberofLepidoptera,self.numberofMantodea,self.numberofMantophasmatodea,self.numberofMecoptera,self.numberofMegaloptera,self.numberofNeuroptera,self.numberofOdonata,self.numberofOrthoptera,self.numberofPhasmatodea,self.numberofPhthiraptera,self.numberofPlecoptera,self.numberofPsocoptera,self.numberofRaphidioptera,self.numberofSiphonaptera,self.numberofStrepsiptera,self.numberofThysanoptera,self.numberofTrichoptera,self.numberofZoraptera]
      
def main():
     
      f = open("insect_transcriptome.txt","r",encoding='utf-8')
      
      labels1 = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008','2007','2006','2005','2004','2003','2002','2001','2000','1999']
      tuplef = Statistics(f)
      '''
      quants1 = tuplef.year()
      xlable1 = 'Year'
      ylable1 = 'the number of papers'
      title1 = 'the insect+transcriptome papers'
      aa = 19
      figure = 1
      draw_bar(labels1,quants1,xlable1,ylable1,title1,aa,figure)
      '''
      lables2 = ['Archaeognatha','Blattodea','Coleoptera','Dermaptera','Diptera','Embioptera','Ephemeroptera','Grylloblattodea','Hemiptera','Hymenoptera','Isoptera','Lepidoptera','Mantodea','Mantophasmatodea','Mecoptera','Megaloptera','Neuroptera','Odonata','Orthoptera','Phasmatodea','Phthiraptera','Plecoptera','Psocoptera','Raphidioptera','Siphonaptera','Strepsiptera','Thysanoptera','Trichoptera','Zoraptera']
      quants2 = tuplef.taxonomy()
      xlable2 = 'insect taxonomy'
      ylable2 = 'the number of papers'
      title2 = 'the insect taxonomy papers'
      aa = 29
      figure = 2
      draw_bar(lables2,quants2,xlable2,ylable2,title2,aa,figure)
if __name__ == "__main__":
      main()
      
            
