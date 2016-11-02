import os.path
import logging
import requests
from twisted.internet import threads


logger = logging.getLogger(__name__)


class SBXSubmitPipeline(object):
    def __init__(self, url, api_key, file_store):
        self.url = url
        self.api_key = api_key
        self.file_store = file_store

    @classmethod
    def from_crawler(cls, crawler):
        url = crawler.settings['SBX_URL']
        api_key = crawler.settings['SBX_API_KEY']
        file_store = crawler.settings['FILES_STORE']
        pipe = cls(url, api_key, file_store)
        pipe.crawler = crawler
        return pipe

    def process_item(self, item, spider):
        dfd = threads.deferToThread(self.submit, item)
        dfd.addBoth(self.item_completed, item)
        return dfd

    def submit(self, item):
        if not item['status']:
            return
        ret = {'status': True}
        absolute_path = os.path.join(self.file_store, item['apk_path'])
        f = open(absolute_path, 'rb')
        buf = f.read()
        f.close()
        headers = {'Content-Type': 'multipart/form-data'}
        data = {
            'apikey': self.api_key,
            'filename': item['apk_path'],
            'file_type': 10,
            'rescan_mode': False,
            'vm_type': 8,
            'platform': 'android',
            'data': buf
        }
        try:
            r = requests.post(self.url, headers=headers, data=data)
            if r.status_code != 200:
                ret['status'] = False
                logger.error(
                    'Submit (error): Error response status[%(status)s]',
                    {'status': r.status_code}
                )
            ret['task_id'] = r.json()['task_id']
        except Exception as e:
            ret['status'] = False
            logger.error(
                'Submit (error): Error request %(err)s',
                {'err': str(e)}
            )
        return ret

    def item_completed(self, result, item):
        if not result:
            return item
        if result['status']:
            item['task_id'] = result['task_id']
        else:
            item['status'] = False
        return item

