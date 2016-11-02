from scrapy import Request
from scrapy.pipelines.files import FilesPipeline


class DownloadPipeline(FilesPipeline):
    EXPIRES = 7
    DEFAULT_FILES_URLS_FIELD = 'apk_url'

    def __init__(self, store_uri, download_func=None, settings=None):
        FilesPipeline.__init__(self, store_uri, self.download, settings)

    def get_media_requests(self, item, info):
        return [Request(item.get(self.files_urls_field),
                        meta={'name': item.get('apk_name')})]

    def file_path(self, request, response=None, info=None):
        return request.meta.get('name') + '.apk'

    def download(self, request, spider):
        return self.crawler.engine.download(request, spider)

    def item_completed(self, results, item, info):
        ok, x = results[0]
        item['status'] = ok
        if ok:
            item['apk_path'] = x['path']
        return item
