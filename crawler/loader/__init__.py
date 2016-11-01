from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity
from .processors import BaseName


class APKItemLoader(ItemLoader):
    default_input_processor = TakeFirst()
    default_output_processor = TakeFirst()
    apk_url_out = Identity()
    apk_name_out = BaseName()

    def load_item(self):
        item = super(APKItemLoader, self).load_item()
        item['apk_file'] = item.get('apk_name') + '.apk'
        return item
