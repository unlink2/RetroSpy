import os
import sys
import util
import urllib


def url_req(url, params, method='GET'):
    if method == 'POST':
        return urllib.request.urlopen(url, data=urllib.parse.urlencode(params))
    else:
        return urllib.request.urlopen(url + '?' + urllib.parse.urlencode(params))

class Updater:
    def __init__(self):
        self.update_available = False
        self.update_url = ''
        self.new_ver = ''

    def check_update(self):
        try:
            url = util.UPDATE_URL
            res = url_req(url, '')
            if res.status == 200:
                res_all = res.read().decode('utf-8')
                res_data = res_all.split('\n')

                if len(res_data) < 2:
                    return
                if Updater.version_str() != res_data[0]:
                    self.update_available = True
                    self.new_ver = res_data[0]
                    self.update_url = res_data[1]
        except Exception as e:
            print(e)

    def download(self):
        pass

    def restart(self):
        os.execl(sys.executable, *([sys.executable] + sys.argv))
        sys.exit(0)

    @staticmethod
    def version_str():
        return '{}.{}.{}'.format(util.VERSION_MAJOR, util.VERSION_MINOR, util.VERSION_PATCH)
