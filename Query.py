# encoding=utf8
import webbrowser
import os

import re
from bs4 import BeautifulSoup
import requests

from wox import Wox, WoxAPI

PKG_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_RESULT = {
    'Title': 'query {url} {keyword}',
    'SubTitle': 'Powered by ousui',
    'IcoPath': 'images/ico.png',
    'JsonRPCAction': {
        'method': '_openUrl',
        'parameters': ['http://github.com/ousui']
    }
}
DEFAULT_HOST = 'http://mvnrepository.com'


class Query(Wox):
    def _request(self, url, stream=False):
        # 如果用户配置了代理，那么可以在这里设置。这里的self.proxy来自Wox封装好的对象
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port")),
                "https": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))}
            return requests.get(url, proxies=proxies, stream=stream)
        else:
            return requests.get(url, stream=stream)

    def _downloadIco(self, url):
        if url.strip() == '':
            return None
        fname = os.path.basename(url)
        fpath = os.path.join(PKG_DIR, 'images', 'cache', fname + '.png')
        if os.path.isfile(fpath):
            return fpath
        resp = self._request(url, stream=True)
        file = open(fpath, 'wb')
        file.write(resp.content)
        file.close()
        return fpath

    def _openUrl(self, url):
        webbrowser.open(url)

    def query(self, query):
        results = []
        keyword = query.strip()
        if keyword == '':
            results.append(DEFAULT_RESULT)
        else:
            tul = re.findall(r'(.*) /(\d+ *)$', query)
            page = 1
            if tul:
                # // 空数组，则 page = 1 否则 pop 0 出来
                pages = tul.pop()
                page = pages[1]
                keyword = pages[0].strip()

            resp = self._request('{}/search?q={}&p={}'.format(DEFAULT_HOST, keyword, page))
            bs = BeautifulSoup(resp.text)
            for el in bs.select('#maincontent > .im'):
                if el.a == None:
                    continue
                uri = el.a['href'];

                ico = self._downloadIco(el.a.img['src'])

                header = el.select('.im-header')[0]
                desc = el.select('.im-description')[0].get_text().strip()
                order = header.select('.im-title > span')[0].get_text().strip()
                title = header.select('.im-title > a')[0].get_text().strip()
                subtitle1 = header.select('.im-subtitle > a')[0].get_text().strip()
                subtitle2 = header.select('.im-subtitle > a')[1].get_text().strip()

                results.append({
                    "Title": '{} {} [{}]'.format(order, title, subtitle1 + ':' + subtitle2),
                    "SubTitle": desc,
                    "IcoPath": ico,
                    "JsonRPCAction": {
                        # 这里除了自已定义的方法，还可以调用Wox的API。调用格式如下：Wox.xxxx方法名
                        # 方法名字可以从这里查阅https://github.com/qianlifeng/Wox/blob/master/Wox.Plugin/IPublicAPI.cs 直接同名方法即可
                        "method": "_openUrl",
                        # 参数必须以数组的形式传过去
                        "parameters": ['{}{}'.format(DEFAULT_HOST, uri)],
                        # 是否隐藏窗口
                        "dontHideAfterAction": True
                    }
                })

        if not results:
            results.append(DEFAULT_RESULT)
        return results


if __name__ == "__main__":
    Query()
