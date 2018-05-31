# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from Github.items import GithubItem, GithubRepoItem
import pymysql


class GithubPipeline(object):
    def __init__(self):
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='666666'
        )
        conn.query('create database if not exists github ')
        conn.commit()
        conn.close()
        self.conn1 = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='666666',
            db='github',
            charset='utf8'
        )

        self.conn1.query('drop table if exists user')
        self.conn1.commit()
        self.conn1.query('drop table if exists repo')
        self.conn1.commit()
        sql_create_table_user = 'create table user (name char(70),repositories int(10),stars int(10),followers int(10),followings int(10))'
        sql_create_table_repo = 'create table repo (repo char(80),fork int(10),star int(10),language char(20))'
        self.conn1.query(sql_create_table_user)
        self.conn1.commit()
        self.conn1.query(sql_create_table_repo)
        self.conn1.commit()
        self.insert_user = 'insert into user(name,repositories,stars,followers,followings) values("{name}","{repositories}","{stars}","{followers}","{followings}")'
        self.insert_repo = 'insert into repo(repo,fork,star,language) values("{repo}","{fork}","{star}","{language}")'

    def process_item(self, item, spider):
        if isinstance(item, GithubItem):
            self.conn1.query(
                self.insert_user.format(
                    name=item['name'],
                    repositories=item['repositories'],
                    stars=item['stars'],
                    followers=item['followers'],
                    followings=item['followings']
                )
            )
            self.conn1.commit()
            return item
        elif isinstance(item, GithubRepoItem):
            self.conn1.query(
                self.insert_repo.format(
                    repo=item['repo'],
                    fork=item['fork'],
                    star=item['star'],
                    language=item['language']
                )

            )
            self.conn1.commit()
            return item

    def close_spider(self, spider):
        self.conn1.close()





