# -*- coding:utf-8 -*-
import csv
import hashlib
import os
import re
from lxml import etree

import requests


class MaFengWo(object):

    def __init__(self):
        self.base_url = "http://www.mafengwo.cn/ajax/router.php"
        self.comments_url = "http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?"
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }

    def save2csv(self,item):
        filepath ='评论.csv'
        if os.path.exists(filepath):
            with open(filepath,'a', encoding='utf-8-sig', newline = '') as f:
                writer = csv.writer(f)
                writer.writerow(item)
        else:
            with open(filepath, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["评论名称","评分星级","评论内容","评论时间"])
                writer.writerow(item)

    def par(self,t):
        hl = hashlib.md5()
        hl.update(t)
        return hl.hexdigest()[2:12]

    def get_comments(self,poi_id):
        for page in range(1,6):
            t = 1579139835337
            qdata = '{"_ts":"' + str(t) + '","params":"{\\"poi_id\\":\\"'+poi_id+'\\",\\"page\\":' + str(page) + ',\\"just_comment\\":1}"}c9d6618dbc657b41a66eb0af952906f1'
            sn = self.par(qdata.encode('utf-8'))
            print(sn)
            querystring = {
                "params": '{"poi_id":'+poi_id+',"page":'+str(page)+',"just_comment":1}',
                "_ts": t,
                "_sn": sn,
                "_": t}

            headers = {
                'Referer': f"http://www.mafengwo.cn/poi/{poi_id}.html",
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
            }

            response = requests.get(self.comments_url, params=querystring, headers=headers)
            data = response.json()
            html= data["data"]["html"]
            e = etree.HTML(html)

            li_tags = e.xpath('//div[@class="rev-list"]/ul/li')
            for each in li_tags:
                # 昵称
                nick_name = each.xpath('./a/text()')[0].strip()
                # 星级
                star = each.xpath('./span/@class')[0].strip()
                star = star.split(' ')[1]
                comments = each.xpath('./p//text()')
                comments = [ item.replace('\n','').strip() for item in comments]
                comments = ''.join(comments).strip()
                # 评论时间
                comment_time = each.xpath('./div[2]/span/text()|./div[3]/span/text()')[0].strip()

                # print(nick_name+'\n',star+'\n',comments+'\n',comment_time)
                item = [nick_name,star,comments,comment_time]

                self.save2csv(item)

    def get_poi_id(self,city_id):
        for page in range(1,301):
            t=1579138712402
            qdata = '{"_ts":"' + str(t) + '","iMddid":"10156","iPage":"' + str(page) + '","iTagId":"0","sAct":"KMdd_StructWebAjax|GetPoisByTag"}c9d6618dbc657b41a66eb0af952906f1'
            sn=self.par(qdata.encode('utf-8'))

            data = {
                'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
                'iMddid': city_id,
                '_ts': t,
                'iPage': page,
                'iTagId': '0',
                '_sn': sn
            }

            response = requests.post(self.base_url, headers=self.headers,data=data)

            # 提取详情页链接
            data = response.json()
            detail_page_tags = data["data"]["list"]
            poi_ids= re.findall('<a href="/poi/(.*?).html"',detail_page_tags,re.S)
            for id in poi_ids:
                self.get_comments(id)


if __name__ == '__main__':
    city_id = '10156'
    mafengwo = MaFengWo()
    mafengwo.get_poi_id(city_id)