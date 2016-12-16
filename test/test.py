#-*- coding: utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup
from selenium import webdriver


htmlCharacterMap = {
    '<br/>' : '\n',
    '&quot;' : '"',
    '&nbsp;' : ' ',
    '&gt;' : '>',
    '&lt;' : '<',
    '&amp;': '&',
    '&#39;':"'",
}

class ELE(object):

    def __init__(self):
        #self.pageIndex = 1
        #self.pagetotal = 9999
        self.cookie = 'aliyungf_tc=AQAAACGP70ZudwwAeVGi06+mpEeyCs1Z; ubt_ssid=k5gxiqcujqltaddeldg7uy1vm8k75dh7_2016-12-16; _utrace=b336fdd7ff5340caa45de10e50e99bc7_2016-12-16; pageReferrInSession=https%3A//www.ele.me/home/; firstEnterUrlInSession=https%3A//www.ele.me/place/wtsqqgt57wp'
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
        self.headers = {'User-Agent' : self.user_agent,'Cookie':self.cookie ,'Host':'www.ele.me','Upgrade-Insecure-Requests':1}
        #self.stories = []
        #self.comments = []
        #self.currentStoryId = ''
        #是否要退出了
        #self.enable = False
        #记录当前是否在查看评论
        #self.viewComment = False

    def getSoup(self):
        soup = BeautifulSoup(open('index.html'),'lxml')
        return soup

    def getInfo(self):
        pass

    def getPageContent(self,url):
        try:
            print url

            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request, timeout=5)
            pageContent = response.read().decode('utf-8')
            return pageContent
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print u"连接饿了吗失败，错误原因：", e.reason
                return None


    def getShopName(self,pageContent):
        soup = BeautifulSoup(pageContent,"lxml")
        print soup
        #shopguide_info = soup.find_all("div",_class=re.compile("shopguide-info-wrapper"))
        #print shopguide_info
        pass

if __name__ == '__main__':
    driver = webdriver.Firefox()
    # print driver
    print driver.get('http://www.jianshu.com/p/520749be7377')
    # ele = ELE()
    # doc = ele.getSoup()
    # doc.prettify()
    #
    # shangjias = doc.find_all("a",class_=re.compile("rstblock"))
    # shopCount = 0
    # shopUrls = []
    # for shangjia in shangjias:
    #     shopCount+=1
    #     shopUrls.append(shangjia.attrs['href'])
    #print shopUrl
    #for shopUrl in shopUrls:
    #ele.getPageContent(shopUrls[0])
    #ele.getShopName()
    #print "商家总数" + str(shopCount)