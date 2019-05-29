# coding=utf-8
from __future__ import print_function

import json
import logging
import os
import time

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}

link_set = set()


class ChromeDownload:
    def __init__(self, har_or_json=None, host=None, dist=None):
        if dist is None:
            self.dist = 'dist/'
        else:
            self.dist = dist
        self.har = har_or_json
        self.host = host

    def find_url(self, obj):
        if not isinstance(obj, dict) and not isinstance(obj, list):
            # print(obj)
            return
        if isinstance(obj, list):
            for v, i in enumerate(obj):
                # print(i)
                if i == 'url':
                    print(v)
                    link_set.add(v)
                else:
                    self.find_url(i)
        if isinstance(obj, dict):
            for i, v in obj.items():
                # print(i)
                if i == 'url':
                    print(v)
                    link_set.add(v)
                else:
                    self.find_url(v)

    def create_folder(self, path):
        path = self.dist + path
        if not os.path.exists(path):
            full = ''
            for pth in os.path.split(path)[0].split('/'):
                full += pth
                if not os.path.exists(path):
                    try:
                        os.mkdir(full)
                    except Exception as e:
                        if 183 not in e.args:
                            logging.exception(e)
                full += os.path.sep
        return path

    def download(self, har_or_json=None, host=None):
        if har_or_json is None:
            har_or_json = self.har
        if host is None:
            host = self.host
        with open(har_or_json) as j:
            jsn = json.loads(j.read())
            # print(jsn)
            self.find_url(jsn)
            print('\n============= LINK ==============\n')
            for link in link_set:
                if host in link:
                    print(link.replace(host, ''))
                    # print(requests.get(link, headers=headers).content)
                    print(os.path.basename(link))
                    s_link = link.replace(host, '')
                    s_link = self.create_folder(s_link)
                    with open(s_link, 'wb') as f:
                        f.write(requests.get(link, headers=headers).content)
                else:
                    print(link)
                    s_link = link.replace('//', '')
                    print(os.path.basename(s_link))
                    s_link = os.path.basename(s_link)
                    if os.path.exists(s_link):
                        s_link = time.time() + s_link
                    s_link = self.create_folder(s_link)
                    with open(s_link, 'wb') as f:
                        try:
                            f.write(requests.get(link, headers=headers, ).content)
                        except Exception as ex:
                            logging.info(u'Error Download {}'.format(link))
                            logging.exception(ex)


if __name__ == '__main__':
    ChromeDownload(r'F:\PYWP\ChromeDownload\localhost.json', 'http://localhost/peise/peise/www.peise.net/').download()
