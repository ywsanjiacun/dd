#encoding:utf-8
import requests
import re

yuan = requests.get('https://tieba.baidu.com/p/5030633687?fr=good').text
demo = re.compile('<a .*?>(.*?)</a>.*?<span class="lzl_content_main">(.*?)*?</span>',re.S)
list = demo.findall(yuan)
print(list[0])
for a,b in list:
    print(a,b)
