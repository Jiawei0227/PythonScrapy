import urllib
import urllib2

user_agent = "XXX"
values = {"username":"wangjiawei0227@163.com","password":"A2wozuida"};
headers = {'User-Agent':user_agent}
data = urllib.urlencode(values)
url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
request = urllib2.Request(url,data,headers)
response = urllib2.urlopen(request)
print response.read()