import hashlib
import requests
def par(t):
    hl = hashlib.md5()
    hl.update(t)
    return hl.hexdigest()[2:12]
page=1
t=1579079437499
poi_id = 30061
qdata='{"_ts":"'+str(t)+'","params":"{\\"poi_id\\":\\"30061\\",\\"page\\":'+str(page)+',\\"just_comment\\":1}"}c9d6618dbc657b41a66eb0af952906f1'
print(qdata)
sn=par(qdata.encode('utf-8'))
print(sn)

url = "http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?"

querystring = {
               "params": '{"poi_id":"30061","page":1,"just_comment":1}',
               "_ts":t,
               "_sn":sn,
               "_":t}

headers = {
    'Referer': "http://www.mafengwo.cn/poi/30061.html",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
# for key,value in querystring.items():
#     url=url+key+'='+str(value)+'&'
# url=url[:-1]
response = requests.get(url,params=querystring, headers=headers)
print(response.json())