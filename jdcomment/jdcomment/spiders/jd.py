# -*- coding: utf-8 -*-
import scrapy
import chardet
import json
import re
from scrapy import Request
from jdcomment.items import JdcommentItem
from lxml import etree

class JdSpider(scrapy.Spider):
    name = "jd"
    # start_urls = ['https://item.jd.com/4142680.html']

    def __init__(self):
        super(JdSpider, self).__init__()
        self.url = 'https://item.jd.com/4378447.html'
        pattern = re.compile('\d+', re.S)
        self.product_id = re.search(pattern, self.url).group()

    def start_requests(self):
        find = input("请输入你要查找的关键字：")
        the_url = 'https://search.jd.com/Search?keyword='+find+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq='+find+'&page=1'
        yield Request(
            url=the_url,
            headers={
                'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Connection':'keep-alive',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
            },
            method='GET',
            dont_filter=True,
            callback=self.zhuaurl
            )

    def zhuaurl(self,response):
        demo = etree.HTML(response.text)
        jiage = demo.xpath('//*[@id="J_goodsList"]/ul/li/div/div[3]/strong/i/text()')
        print(len(jiage))
        num = demo.xpath('//*[@id="J_goodsList"]/ul/li/div/div[4]/a/@href')
        print(len(num))
        guang = demo.xpath('//*[@id="J_goodsList"]/ul/li/div/span/text()')
        print(len(guang))
        # url = demo.xpath('//*[@id="J_goodsList"]/ul/li/div/div[1]/a/@href')
        # for i  in  url :
        #     print(i)
    # def start_requests(self):
    #
    #     yield Request(
    #         url=self.url,
    #         headers={
    #             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #             'Accept-Encoding': 'gzip, deflate, br',
    #             'Accept-Language': 'en-US,en;q=0.5',
    #             'Connection': 'keep-alive',
    #             'Host': 'item.jd.com',
    #             'Upgrade-Insecure-Requests': '1',
    #             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 '
    #                           'Firefox/52.0',
    #         },
    #         method='GET',
    #         dont_filter=True,
    #         callback=self.get_comment_count
    #     )
    # 向接口传参数进行请求，实现链接拼接
    # def get_comment_count(self,response):
    #     pattern = re.compile('commentVersion:\'(\d+)\'', re.S)
    #     comment_version = re.search(pattern, response.text).group(1)
    #     # 5 是推薦排序， 6是按照時間排序
    #     url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv' \
    #           '{comment_version}&productId={product_id}&score=0&sortType={sort_type}&page=0&pageSize=10' \
    #           '&isShadowSku=0'. \
    #         format(product_id = self.product_id, comment_version = comment_version, sort_type = '6')
    #     yield Request(
    #         url=url,
    #         headers={
    #             'Accept': '*/*',
    #             'Accept-Encoding': 'gzip, deflate, br',
    #             'Accept-Language': 'en-US,en;q=0.5',
    #             'Connection': 'keep-alive',
    #             'Host': 'club.jd.com',
    #             'Referer': 'https://item.jd.com/%s.html' % self.product_id, # 引用的url
    #             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 '
    #                           'Firefox/52.0',
    #         },
    #         method='GET',
    #         callback=self.get_all_comment
    #     )
    #
    # # 实现分页
    # def get_all_comment(self,response):
    #     pattern = re.compile('\((.*?)\);', re.S)
    #     items = re.search(pattern, response.text)
    #     if items != None and items.group(1) != None:
    #         data = json.loads(items.group(1))
    #         pcs = data.get('productCommentSummary')
    #         comment_count = pcs.get('commentCount')
    #         comment_version = response.meta.get('comment_version')
    #         # 分頁拼接链接
    #         for i in range(0, int(int(comment_count)/10)):
    #             url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv' \
    #                   '{comment_version}&productId={product_id}&score=0&sortType={sort_type}&page={page}&' \
    #                   'pageSize=10&isShadowSku=0'. \
    #                 format(product_id=self.product_id, comment_version=comment_version, sort_type='5',
    #                        page=i)
    #             yield Request(
    #                 url=url,
    #                 headers={
    #                     'Accept': '*/*',
    #                     'Accept-Encoding': 'gzip, deflate, br',
    #                     'Accept-Language': 'en-US,en;q=0.5',
    #                     'Connection': 'keep-alive',
    #                     'Host': 'club.jd.com',
    #                     'Referer': 'https://item.jd.com/%s.html' % self.product_id,  # 引用的url
    #                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 '
    #                                   'Firefox/52.0',
    #                 },
    #                 method='GET',
    #                 callback=self.get_comment_info,
    #                 meta = {'page':i+1}
    #             )
    #
    # # 解析详细内容
    # def get_comment_info(self,response):
    #     item = JdcommentItem()
    #     detect = chardet.detect(response.body)
    #     encoding = detect.get('encoding', '')
    #     body = response.body.decode(encoding, 'ignore')
    #     pattern = re.compile('\((.*?)\);', re.S)
    #     items = re.search(pattern, body)
    #     dictss = {}
    #     listss = []
    #     if items != None and items.group(1) != None:
    #         data = json.loads(items.group(1))
    #         # 物品总评论信息
    #         pcs = data.get('productCommentSummary')
    #         product_info = {
    #             'comment_count': pcs.get('commentCount'), # 评论数
    #             'good_count': pcs.get('goodCount'),# 好评数
    #             'gen_count': pcs.get('generalCount'), # 中评
    #             'bad_count': pcs.get('poorCount'),# 差评
    #             'add_count': pcs.get('afterCount'),# 追评
    #             'show_img_count': pcs.get('imageListCount'),
    #             'page' : response.meta['page']
    #         }
    #         print(product_info)
    #         dictss['product_info'] = product_info
    #         #用户信息
    #         comments = data.get('comments') # 返回list
    #         for comment in comments:
    #             user_info = {
    #                 'user_id': comment.get('id'),# 用户id
    #                 'content': comment.get('content'),
    #                 'useful_vote_count': comment.get('usefulVoteCount')  # 其他用户觉得有用的数量
    #             }
    #             print(user_info)
    #             print('------------------------------')
    #             listss.append(user_info)
    #         dictss['user_info'] = listss
    #         item['com_info'] = dictss
    #         yield item

