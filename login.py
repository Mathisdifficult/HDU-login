# encoding=utf-8
#copyright (c)YLZ admin@0509.uu.me 
import urllib
import urllib2
import re
from pyquery import PyQuery as pq
from lxml import etree
import os
import string
import StringIO
import cookielib 
import hashlib
import getpass

username=""
password=""
host="http://jxglteacher.hdu.edu.cn/"
STUrl=""
session=""
name=""
classlist={}
classres=""
onhook=0
gnmkdm=""
aspxsession=""


def md5(src):
    global password
    myMd5 = hashlib.md5()
    myMd5.update(src)
    password = myMd5.hexdigest()
def getsession():
    try:
        global session,hosturl,aspxsession
        openres=urllib2.urlopen(urllib2.Request(url = host))
        openurl=openres.geturl()
        if ")" in openurl and "(" in openurl:
            mylist= re.findall(r"(?<=\().*?(?=\))",openurl,re.DOTALL)
            session= mylist[0]
            print u"成功获取session:"+session
            hosturl=host+'('+session+')/'
        else:
            hosturl=host
            print u"服务器连接正常"
            aspxsession = re.findall(r"^.*?(?=; path=/)",openres.info().getheader('Set-Cookie'),re.DOTALL)[0]
    except:
        return 0
    return 1

#urllib函数，用于提交http数据
def open(aurl,post='',Referer=''):
    #proxy = 'http://127.0.0.1:8088'
    #opener = urllib2.build_opener( urllib2.ProxyHandler({'http':proxy}) )
    #urllib2.install_opener(opener)
    if post!='':
        test_data_urlencode = urllib.urlencode(post)
        req = urllib2.Request(url=aurl,data = test_data_urlencode)
    else:
        req = urllib2.Request(url=aurl)
    if Referer!='':
        req.add_header('Referer',Referer)
    if aspxsession!="":
        req.add_header('Cookie',aspxsession)
    res_data = urllib2.urlopen(req)
    return res_data

def login():
#post数据接收和处理的页面
	posturl = "http://cas.hdu.edu.cn/cas/login"
	loginpage = 'http://cas.hdu.edu.cn/cas/login?service=http://jxglteacher.hdu.edu.cn/index.aspx'
	url = 'http://jxglteacher.hdu.edu.cn'

	headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 QQ/6.7.1.416 V1_IPH_SQ_6.7.1_1_APP_A Pixel/750 Core/UIWebView NetType/4G QBWebViewType/1',
             'Referer' : 'http://cas.hdu.edu.cn/cas/login?service=http://jxglteacher.hdu.edu.cn/index.aspx'} 


	response = urllib2.urlopen(loginpage)  
	text = response.read()  
	#print text
	S = re.findall(r'\w{2}-\d{6}-\w{20}',text)
	loginticket = S[0]
	postData = {'encodedService' : 'http%3a%2f%2fjxglteacher.hdu.edu.cn%2findex.aspx',  
            'service' : 'http://jxglteacher.hdu.edu.cn/index.aspx',  
            'serviceName' : 'null', 
            'loginErrCnt' : '0', 
            'username' : username,   
            'password' : password,
            'lt' : loginticket
        
            } 

	cj = cookielib.LWPCookieJar()  
	cookie_support = urllib2.HTTPCookieProcessor(cj)  
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
	urllib2.install_opener(opener)  
	#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）  
	h = urllib2.urlopen(loginpage)  
	#需要给Post数据编码  
	postData = urllib.urlencode(postData)  
	  
	#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
	request = urllib2.Request(posturl, postData, headers)  
	#print request  
	response = urllib2.urlopen(request)  
	text = response.read()  
	#print text  
	S = re.findall(r'\w{2}-\d{6}-\w{20}',text)
	
	STUrl='http://jxglteacher.hdu.edu.cn/index.aspx?ticket='+S[1]
	print STUrl 
	#print request
	
#程序初始化登录函数
def init():
    global username,password

    username=raw_input("username:")
    password=raw_input("password:")
    md5(password)
	
if __name__ == '__main__':
	while not getsession():
		print u"session获取失败，正在重试"
	init()
	login()
	raw_input(unicode('按回车键退出...','utf-8').encode('gbk'))
