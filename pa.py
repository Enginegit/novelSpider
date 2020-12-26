import requests
import re
#import time
""" import random
from fake_useragent import UserAgent
ua = UserAgent()
header = {'User-Agent': ua.chrome} """
linelist={}
www = int(input("什么网站？1.笔趣网 2.趣书吧"))
if www == 1:
    encoding='utf-8'
elif www == 2:
    encoding='gbk'
web = input("哪个网址开始爬？")
count = int(input("搞几章？"))
""" r = requests.get(web,headers=header) """
r = requests.get(web)
r.encoding=encoding
try:
    if www==1:
        name = re.search(r'var booktitle = "(.*?)"',r.text).group().split('"')[1]
    elif www==2:
        name = re.search(r'var booktitle="(.*?)"',r.text).group().split('"')[1]
except:
    print('\n')
    print('匹配不到书名')
    print(r.text)

print('《'+name+'》')

for n in range(0,count):
    """  r = requests.get(web,headers=header) """
    while True:
        r = requests.get(web)
        r.encoding=encoding
        try:
            if www==1:
                title=re.search(r'var readtitle = "(.*?)"',r.text).group().split('"')[1]
                print(title)
                break
            elif www==2:
                title=re.search(r'var readtitle="(.*?)"',r.text).group().split('"')[1]
                print(title)
                break
        except:
            """ print('\n')
            print('匹配不到标题')
            print(r.text) """
            continue
        
    try:
        if www==1:
            txt = re.search(r'<div id="content"><!--go-->\r\n(.*?)<!--over-->',r.text)
            linelist = txt.group().split('<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;')
            linelist[0] = linelist[0].split('&nbsp;&nbsp;&nbsp;&nbsp;')[1]
            linelist[-1] = linelist[-1].split('<!--over-->')[0]
        elif www==2:
            txt = re.search(r'<div id="content">(.*?)</div>',r.text)
            linelist = txt.group().split('<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;')
            linelist[0] = linelist[0].split('&nbsp;&nbsp;&nbsp;&nbsp;')[1]
            linelist[-1] = linelist[-1].split('</div>')[0]
    except:
        print('\n')
        print('匹配不到内容')
        print(r.text)

    with open(name+'.txt','a',encoding="utf-8") as f:
        f.write('\t')
        f.write(title)
        f.write('\n\n')
        for line in linelist:
            f.write('  ')
            f.write(line)
            f.write('\n')
        f.write('\n')
    if www==1:
        result = re.search(r'next_page = "(.*?)";var index_page = "(.*?)"',r.text)
        web = result.group().split('"')[3]+result.group().split('"')[1]
    elif www==2:
        result = re.search(r'next_page = "(.*?)";\r\nvar index_page = "(.*?)"',r.text)
        web = "http://qushuba.net"+result.group().split('"')[1]