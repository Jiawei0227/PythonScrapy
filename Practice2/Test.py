# -×- coding: utf-8 -*-
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


class BDTB:
    def __init__(self,baseURL,seeLz):
        self.baseURL = baseURL
        self.seeLZ = '?see_lz='+str(seeLz)
        self.tool = Tool()

    def getPage(self,pageNum):
        try:
            url = self.baseURL+self.seeLZ+'&pn='+str(pageNum)
            #print url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)

            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败，错误原因",e.reason
                return None

    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1)
        else:
            return None

    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num.*?><span class="red".*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1)
        else:
            return None

    def getContent(self,page):
        content = self.getPage(page)
        pattern = r'<div id="post_content_.*?>(.*?)</div>'
        result = re.findall(pattern,content)
        for item in result:
            print '------------------------------楼--------------------------------------'
            print self.tool.replace(item)
        return

    def start(self):
        #print u'Title:'+ self.getTitle()
        #print u'TotalReply:'+str(self.getPageNum())
        print 'Content:'
        self.getContent(1)

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()


baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL,1)
bdtb.start()