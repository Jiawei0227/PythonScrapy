import urllib2
#
# request = urllib2.Request("http://www.baidu.com")
# response = urllib2.urlopen(request)
# print response.read()

# enable_proxy = True
# proxy_handler = urllib2.ProxyHandler({"http":'http://some-proxy:8080'})
# null_proxy_handler = urllib2.ProxyHandler({})
# if enable_proxy:
#     opener = urllib2.build_opener(proxy_handler)
# else:
#     opener = urllib2.build_opener(null_proxy_handler)
# urllib2.install_opener(opener)

req = urllib2.Request('http://blog.csdn.net/cqcre')
try:
    urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.code
    print e.reason