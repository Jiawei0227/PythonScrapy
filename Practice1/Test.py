# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

htmlCharacterMap = {
    '<br/>' : '\n',
    '&quot;' : '"',
    '&nbsp;' : ' ',
    '&gt;' : '>',
    '&lt;' : '<',
    '&amp;': '&',
    '&#39;':"'",
}

class QSBK:
    def printContent(self):
        page = 1
        url = 'http://www.qiushibaike.com/'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        try:
            request = urllib2.Request(url,headers = headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            pattrenStr = r'<h2>(?P<authorname>.*?)</h2>.*?' \
                         r'<div class="articleGender (?P<gender>.*?)Icon">(?P<age>.*?)</div>.*?' \
                         r'<div class="content">\s*<span>(?P<content>.*?)</span>\s*</div>' \
                         r'(?P<maybehaveimage>.*?)' \
                         r'<i class="number">(?P<numbervote>.*?)</i>.*?' \
                         r'<span class="stats-comments">(?P<comments>.*?)</div>'
            pattern = re.compile(pattrenStr,re.S)
            items = re.findall(pattern,content)


            for item in items:
                haveImg = re.search("img",item[4])
                if haveImg:
                    continue
                content = item[3].strip()
                for (k,v) in htmlCharacterMap.items():
                    content = re.sub(re.compile(k), v, content)
                authorname = item[0].strip()
                for (k,v) in htmlCharacterMap.items():
                    authorname = re.sub(re.compile(k), v, authorname)

                pattern = re.compile(r'<a href="/article/(?P<id>.*?)".*?<i class="number">(?P<comment>.*?)</i>',re.S)
                commentItems = re.findall(pattern,item[6])

                print 'Auther:'+authorname+' Gender:'+item[1]+' Age:'+item[2]+'\n'+'Content:'+content+'\n'+'Like:'+item[5]+'\n'+'CommentNumber:'+commentItems[0][1]+'\n'

                #print item[4]

        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason

if __name__ == '__main__':
    test = QSBK()
    test.printContent()