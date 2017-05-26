#-*- coding: utf-8 -*-

import urllib2
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import sys


class ELE(object):

    def __init__(self):
        self.cookie = 'aliyungf_tc=AQAAACGP70ZudwwAeVGi06+mpEeyCs1Z; ubt_ssid=k5gxiqcujqltaddeldg7uy1vm8k75dh7_2016-12-16; _utrace=b336fdd7ff5340caa45de10e50e99bc7_2016-12-16; pageReferrInSession=https%3A//www.ele.me/home/; firstEnterUrlInSession=https%3A//www.ele.me/place/wtsqqgt57wp'
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
        self.headers = {'User-Agent' : self.user_agent,'Cookie':self.cookie ,'Host':'www.ele.me','Upgrade-Insecure-Requests':1}


    def getSoup(self):
        soup = BeautifulSoup(open('index.html'),'lxml')
        return soup

    def getPageContent(self,url):
        try:
            print url
            driver = webdriver.PhantomJS()
            driver.get(url)
            pageContent = driver.page_source
            driver.quit()
            return pageContent

        except Exception, e:
            if hasattr(e, 'reason'):
                print u"连接饿了吗失败，错误原因：", e.reason
                return None

    def getNumberfromString(self,s):
        s = re.findall(r"\d+\.?\d*",s)
        return s

    def getPopularFood(self,soup):
        popularFood = soup.find_all("h3",class_="shopmenu-title ng-binding")[0]
        popularFoods = []
        while popularFood.next_sibling.string != " end ngRepeat: food in category.foods ":
            if popularFood.find_next_sibling("div",class_="shopmenu-food ng-isolate-scope") != None:
                popularFood = popularFood.find_next_sibling("div",class_="shopmenu-food ng-isolate-scope")
            else:
                popularFood = popularFood.find_next_sibling("div",class_="shopmenu-food ng-isolate-scope noimg")

            popularFoodName = popularFood.div.h3.string
            popularFoodSellperMonth = popularFood.div.find_all("span", class_="color-mute ng-binding")[1].string
            popularFoodPrice = popularFood.find("span",class_="col-3 shopmenu-food-price color-stress ng-binding")
            #print popularFoodPrice
            pricepattern = re.compile('<span class="col-3 shopmenu-food-price color-stress ng-binding">(.*?)<small class="ng-binding">.*?</small></span>', re.S)
            popularFoodPrice = re.search(pricepattern, str(popularFoodPrice)).group(1).strip()
            popularFoods.append({'popularFoodName':popularFoodName,'popularFoodPrice':popularFoodPrice,'popularFoodSellperMonth':popularFoodSellperMonth})

        return popularFoods



    def getShopBadComment(self,id):
        #pageContent = self.getPageContent(url)
        #soup = BeautifulSoup(pageContent,"lxml")
        url = 'https://mainsite-restapi.ele.me/ugc/v1/restaurant/'+id+'/ratings?limit=999&offset=0&record_type=3'
        f = urllib2.urlopen(url)
        badComments = json.load(f)

        badCommentInfo = []
        for badComment in badComments:
            #print badComment
            if badComment['rating_text'] == "":
                continue
            badCommentInfo.append(badComment['rating_text'])

        # for badComment in badCommentInfo:
        #     print badComment

        return badCommentInfo


    def getShopInfo(self,url):
        pageContent = self.getPageContent(url)
        soup = BeautifulSoup(pageContent,"lxml")

        shopguide_info = soup.find("div",class_="shopguide-info-wrapper")
        #print shopguide_info[0]
        shopname = shopguide_info.div.h1.attrs['title']

        shopCommentNum = shopguide_info.find("a",class_="ng-binding").string

        shopSellperMonth = shopguide_info.find("span",class_="ng-binding").string
        shopSellperMonth = self.getNumberfromString(shopSellperMonth)

        shopguide_info_extra = soup.find("div",class_="shopguide-info-extra")

        shopZonghe = shopguide_info_extra.find("h2",class_="color-stress ng-binding").string

        shopAttitudeScore = shopguide_info_extra.find("div",rating="shopRatingScore.service_score").attrs['title']
        shopAttitudeScore = self.getNumberfromString(shopAttitudeScore)

        shopFoodScore = shopguide_info_extra.find("div",rating="shopRatingScore.food_score").attrs['title']
        shopFoodScore = self.getNumberfromString(shopFoodScore)

        shopTime = soup.find_all("em",class_="shopguide-server-value ng-binding")[2].string
        shopTime = self.getNumberfromString(shopTime)

        #获取热门服务
        shopPopular = self.getPopularFood(soup)

        #获取不满意的所有评价
        id = url.split("/")[-1]

        shopBadComment = self.getShopBadComment(id)


        shopInfo = {'shopname':shopname,'shopCommentNum':shopCommentNum,u'shopSellperMonth':shopSellperMonth,'shopZongheScore':shopZonghe,
                    'shopAttitudeScore':shopAttitudeScore,'shopFoodScore':shopFoodScore,'shopTime':shopTime,'poplarFood':shopPopular,'shopBadComment':shopBadComment}
        print shopInfo
        return shopInfo



if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    ele = ELE()
    doc = ele.getSoup()
    doc.prettify()
    shopInfos = []
    shangjias = doc.find_all("a",class_=re.compile("rstblock"))
    shopCount = 0
    shopUrls = []
    for shangjia in shangjias:
        shopCount+=1
        shopUrls.append(shangjia.attrs['href'])

    f = open("data.json","a+")
    count = 160
    while count<168:
    #    ele.getShopInfo(shopUrls[count])
        f.write(json.dumps(ele.getShopInfo(shopUrls[count]),ensure_ascii=False))
        f.write(',')
        f.write('\n')
        count+=1

    f.close()
    #for shopInfo in shopInfos:
        


    print "商家总数" + str(shopCount)