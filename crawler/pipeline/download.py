import requests
import json
from scrapy import Request
from scrapy.pipelines.files import FilesPipeline, FSFilesStore, S3FilesStore
from twisted.internet import threads


class SBoxFilesStore(object):
    def __init__(self, uri):
        assert uri.startswith('sbx://')
        self.api_key = '2E2B1D28D7CB3EA69A0712BC3B0445ED'
        self.url = 'http://' + uri.split('://')[-1]

    def stat_file(self, path, info):
        return None

    def persist_file(self, path, buf, info, meta=None, headers=None):
        buf.seek(0)
        return threads.deferToThread(self.put_object, headers, path, buf)

    def put_object(self, headers, filename, body):
        extra = {'Content-Type': 'multipart/form-data'}
        if headers:
            extra.update(headers)
        data = {
            'apikey': self.api_key,
            'filename': filename,
            'file_type': 10,
            'rescan_mode': False,
            'vm_type': 8,
            'platform': 'android',
            'data': body
        }
        r = requests.post(self.url, headers=headers, data=json.dumps(data))
        assert r.status_code == 200


class DownloadPipeline(FilesPipeline):
    EXPIRES = 7
    DEFAULT_FILES_URLS_FIELD = 'apk_url'
    STORE_SCHEMES = {
        '': FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'sbx': SBoxFilesStore,
    }

    def __init__(self, store_uri, download_func=None, settings=None):
        FilesPipeline.__init__(self, store_uri, self.download, settings)

    def get_media_requests(self, item, info):
        return [Request(x, meta={'file': item.get('apk_file')})
                for x in item.get(self.files_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        return request.meta.get('file')

    def download(self, request, spider):
        return self.crawler.engine.download(request, spider)
