# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from Github.items import GithubItem, GithubRepoItem
import requests
from lxml import etree
import random
from Github.settings import USER_AGENTS


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    user = 'ChenPY95'

    # 获取用户指定页数的followers
    def get_urls(self, u, *, start=1, stop=2):
        users = []
        for p in range(start, stop+1):
            response = requests.get(u + '?page=' + str(p) + '&tab=followers',
                                    headers={'User-Agent': random.choice(USER_AGENTS)})
            root = etree.HTML(response.text)
            for user in root.xpath('//span[@class="link-gray pl-1"]/text()'):
                users.append(user)
            try:  # 检查有没有下一页
                root.xpath('//a[text()="Next"]/@href')[0]
            except:
                break

        return users

    # 获取用户仓库信息
    def get_repos(self, u, *, start=1, stop=3):
        repos = []
        for p in range(start, stop+1):
            response = requests.get(u + '?page=' + str(p) + '&tab=repositories',
                                    headers={'User-Agent': random.choice(USER_AGENTS)})
            root = etree.HTML(response.text)
            for repo in root.xpath('//li[@class="col-12 d-block width-full py-4 border-bottom public source"]'):
                name = repo.xpath('./div/h3/a/@href')[0]
                stars = repo.xpath('./div[@class="f6 text-gray mt-2"]/a[@href="' + name + '/stargazers"]/text()')
                if stars:
                    star = stars[-1].split()[0]
                    if star[-1] == 'k':
                        star = int(float(star[:-1])*1000)
                else:
                    star = 0
                forks = repo.xpath('./div[@class="f6 text-gray mt-2"]/a[@href="' + name + '/network"]/text()')
                if forks:
                    fork = forks[-1].split()[0]
                    if fork[-1] == 'k':
                        fork = int(float(star[:-1])*1000)
                else:
                    fork = 0
                language = repo.xpath('./div[@class="f6 text-gray mt-2"]/span[@class="mr-3"]/text()')
                if language:
                    language = language[0].split()[0]
                else:
                    language = ''
                repos.append(('https://github.com' + name, star, fork, language))

            try:
                root.xpath('//a[text()="Next"]/@href')[0]
            except:
                break

        return repos

    def start_requests(self):
        yield Request(url='https://github.com/' + self.user + '?tab=followers',
                      callback=self.parse)

    def parse(self, response):
        item = GithubItem()
        user = response.url.split('?')[0]
        item['name'] = user
        nav = response.xpath('//nav[@class="UnderlineNav-body"]')[0]

        repositories = nav.xpath('./a[@title="Repositories"]/span/text()')[0].extract().split()[0]
        if repositories[-1] == 'k':
            repositories = float(repositories[:-1])*1000
        item['repositories'] = int(repositories)

        stars = nav.xpath('./a[@title="Stars"]/span/text()')[0].extract().split()[0]
        if stars[-1] == 'k':
            stars = float(stars[:-1])*1000
        item['stars'] = int(stars)

        followers = nav.xpath('./a[@title="Followers"]/span/text()')[0].extract().split()[0]
        if followers[-1] == 'k':
            followers = float(followers[:-1])*1000
        item['followers'] = int(followers)

        followings = nav.xpath('./a[@title="Following"]/span/text()')[0].extract().split()[0]
        if followings[-1] == 'k':
            followings = float(followings[:-1])*1000
        item['followings'] = int(followings)

        yield item

        for repo in self.get_repos(user):
            item = GithubRepoItem()
            item['repo'] = repo[0]
            item['star'] = repo[1]
            item['fork'] = repo[2]
            item['language'] = repo[3]
            yield item

        for u in self.get_urls(user):
            yield Request(url='https://github.com/' + u + '?tab=followers',
                          callback=self.parse, dont_filter=False)



