# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lxml import etree

class CiSpider(scrapy.Spider):
    name = 'ci'
    allowed_domains = ['www.xicidaili.com/']
    start_urls = 'http://www.xicidaili.com//'

    def start_requests(self):
        yield Request(self.start_urls,self.parse)

    def parse(self, response):
        demo = etree.HTML(response.text)
        for i in range(2,22):
            ip = demo.xpath('//*[@id="ip_list"]/tbody/tr['+str(i)+']/td[2]/text()')
            port = demo.xpath('//*[@id="ip_list"]/tbody/tr['+str(i)+']/td[3]/text()')
            address = demo.xpath('//*[@id="ip_list"]/tbody/tr['+str(i)+']/td[4]/text()')
            niming = demo.xpath('//*[@id="ip_list"]/tbody/tr['+str(i)+']/td[5]/text()')
            style = demo.xpath('//*[@id="ip_list"]/tbody/tr['+str(i)+']/td[6]/text()')
            cunhuo_time = demo.xpath('//*[@id="ip_list"]/tbody/tr['+str(i)+']/td[7]/text()')
            yanzheng_time = demo.xpath('//*[@id="ip_list"]/tbody/tr['+str(i)+']/td[8]/text()')
            print(ip,port)