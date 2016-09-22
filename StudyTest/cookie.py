#-*- coding:utf8 -*-
import urllib
import urllib2
import cookielib

filename = 'cookie.txt'
#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
#cookie = cookielib.MozillaCookieJar(filename)

#创建MozillaCookieJar实例对象
cookie = cookielib.MozillaCookieJar()
#从文件中读取cookie内容到变量
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
# postdata = urllib.urlencode({
# 			'userName':'141250136',
# 			'password':'317317'
# 		})
#登录教务系统的URL
# loginUrl = 'http://jwas2.nju.edu.cn:8080/jiaowu/login.do'
#模拟登录，并把cookie保存到变量
# result = opener.open(loginUrl,postdata)
#保存cookie到cookie.txt中
# cookie.save(ignore_discard=True, ignore_expires=True)
#利用cookie请求访问另一个网址，此网址是成绩查询网址
gradeUrl = 'http://jwas2.nju.edu.cn:8080/jiaowu/student/studentinfo/achievementinfo.do?method=searchTermList'
#请求访问成绩查询网址
result = opener.open(gradeUrl)
print result.read()