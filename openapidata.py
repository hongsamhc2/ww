import re
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import Request, urlopen
from urllib.parse import urlencode,quote_plus,unquote
from datetime import datetime
import os
def get_data(url,queryParams):
    pattern = re.compile(('<([ㄱ-ㅣ가-힣]+)>'))

    request_url = Request(url + queryParams)
    data_dic = {}
    request_url.get_method = lambda: 'GET'
    response_body = urlopen(request_url).read()
    soup = BeautifulSoup(response_body, 'lxml-xml')
    item_contents = soup.findAll('item')
    print(soup.find('resultCode'))
    for content in item_contents:

        for i in range(len(content)):
            data = content.contents[i]
            tag = re.match(pattern,str(data)).group()
            replace_tag = re.sub(pattern,'\\1',tag)
            if replace_tag not in data_dic.keys():
                data_dic[replace_tag] = [data.get_text().strip()]
            else:
                data_dic[replace_tag] += [data.get_text().strip()]
    if len(data_dic) == 0:
        df = []
    else:
        df = pd.DataFrame.from_dict(data_dic,orient='index')
        df = df.T
        print(df)
    return df


code_list = ['11110']
YM_list = []
now = datetime.today()
now_str = now.strftime('%Y%m')
YM_list.append(now_str)
now_int = int(now_str)
prev = now_int -1
for i in range(240):

    if prev %100 ==0:
        prev = prev -100 +12
    YM_list.append(str(prev))
    prev -= 1




url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
key = key = unquote('0RZwX%2BuD34DcTTK3adGbpiohmzlPjeJA26pc9Pqp0UFxQFi3mInkeBK8C%2Bklf8XlXSTyoEnmUQAeNmGMFUBFNw%3D%3D')

for code in code_list:
    for YM in YM_list:
        if os.path.isfile(f'.\\DB\\{code}_{YM}.csv'):
            continue
        queryParams = '?' + urlencode({ quote_plus('ServiceKey'):key,
                                        quote_plus('LAWD_CD'):code,
                                        quote_plus('DEAL_YMD'):YM})
        df = get_data(url,queryParams)
        if len(df) == 0:
            break
        df.to_csv(f'.\\DB\\{code}_{YM}.csv',encoding='utf-8-sig',index=False)

