# -*- coding: utf-8 -*-
import scrapy

from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名称，不能和项目重复
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口url, 写入调度器里面
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        """解析下载器下载下来的数据"""
        # 循环电影条目
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for movie in movie_list:
            # 导入item文件，类似django的模型
            douban_item = DoubanItem()
            douban_item['serial_number'] = movie.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = movie.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()

            intruduces = movie.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            for content in intruduces:
                douban_item['introduce'] = ''.join(content.split())

            douban_item['star'] = movie.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = movie.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = movie.xpath(".//p[@class='quote']/span/text()").extract_first()

            # 需要将数据yield到piplines里面进行下一步的数据处理和存储
            yield douban_item

        # 解析下一页规则
        next_link = response.xpath("//span[@class='next']/link/@href").extract()

        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)



