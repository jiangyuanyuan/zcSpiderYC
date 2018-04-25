# -*- coding: utf-8 -*-
import scrapy

from zcSpider.items import ZcspiderItem


class DongdongSpider(scrapy.Spider):
    name = 'zu'
    allowed_domains = ['zgzcw.com']
    url = 'http://news.zgzcw.com/zc/zx_1.shtml'
    offset = 2952
    start_urls = [url]


    def parse(self, response):
        # 每一页里的所有帖子的链接集合
        # links = response.xpath('//div[@id="ctl09_divList_1"]//tbody//a[contains(@href,"info")]').extract()
        #
        # # 迭代取出集合里的链接
        # for link in links:
        #     if link != '':
        #         # 提取列表里每个帖子的链接，发送请求放到请求队列里,并调用self.parse_item来处理
        #         # print link
        # yield scrapy.Request(link, callback = self.parse_item)

        item = ZcspiderItem()
        # 标题
        # item['title'] = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract()[0]
        item['title'] = response.xpath('//div[@class="news-left2"]//h1/text()').extract()[0]
        # 时间
        timecontent = ""
        time = response.xpath('//div[@class="news-left2"]//div[@class="cont-bt-ly"]//span/text()').extract()
        for ti in time:
            timecontent = timecontent + ti
        item['time'] = timecontent
        # 内容，先使用有图片情况下的匹配规则，如果有内容，返回所有内容的列表集合
        contents = response.xpath('//div[@class="news-left2"]//div[@class="cont-txt"]//div/text()').extract()
        contents1 = response.xpath('//div[@class="news-left2"]//div[@class="cont-txt"]//p/text()').extract()
        contents2 = response.xpath('//div[@class="news-left2"]//div[@class="cont-txt"]//span/text()').extract()
        # contents1 = response.xpath('//div[@class="z_left"]//div[@class="text"]//span//strong/text()').extract()
        content = ""
        for cont in contents1:
            content = content+cont
        for cont in contents2:
            content = content + cont
        for cont in contents:
            content = content + cont
        item['content'] = content
        # print content
        item['url'] = response.url
        yield item
        while (self.offset > 1):
            self.offset = self.offset -1
            # 发送请求放到请求队列里，调用self.parse处理response
            yield scrapy.Request("http://news.zgzcw.com/zc/zx_" +str(self.offset)+".shtml", callback = self.parse)


