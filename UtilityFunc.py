import re
from urllib.request import Request, urlopen
import pandas as pd
from bs4 import BeautifulSoup


def get_data(url,queryParams):
    pattern = re.compile(('<([ㄱ-ㅣ가-힣]+)>'))

    request_url = Request(url + queryParams)
    data_dic = {}
    request_url.get_method = lambda: 'GET'
    response_body = urlopen(request_url).read()
    soup = BeautifulSoup(response_body, 'lxml-xml')
    header_code = soup.find('resultCode').get_text()
    item_contents = soup.findAll('item')
    print(soup.find('header'))
    for content in item_contents:
        for i in range(len(content)):
            data = content.contents[i]
            tag = re.match(pattern,str(data)).group()
            replace_tag = re.sub(pattern,'\\1',tag)
            if replace_tag not in data_dic.keys():
                data_dic[replace_tag] = [data.get_text().strip()]
            else:
                data_dic[replace_tag] += [data.get_text().strip()]
    if len(data_dic) != 0 and header_code == '00':
        df = pd.DataFrame.from_dict(data_dic,orient='index')
    else:
        df = header_code
    return df