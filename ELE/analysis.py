#-*- coding: utf-8 -*-
import json


def getData():
    with open('data.json') as json_file:
        data = json.load(json_file)
    return data

if __name__ == '__main__':
    shopData = getData()
    for shop in shopData:
        #e.g. 获取商店名字
        print '-------------------------'+shop['shopname']+'----------------------------'

        #e.g. 获取商店差评
        for badComment in shop['shopBadComment']:
            print badComment

        ## 分析操作...