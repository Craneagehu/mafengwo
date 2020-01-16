# mafengwo
马蜂窝 这个网站 最大的技术难点就是怎么 破解 _sn 参数的 MD5 加密。无论是获取详情页信息还是 评论信息，都会用到这个 参数。
重点：
通过 找到 index.js?1552035728 这个js文件，经过断点调试 可以获取 加密过程。

        def par(t):
            hl = hashlib.md5()
            hl.update(t)
            return hl.hexdigest()[2:12]
        
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
