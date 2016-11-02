from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity
from .processors import BaseName


class APKItemLoader(ItemLoader):
    default_input_processor = TakeFirst()
    default_output_processor = TakeFirst()
    apk_name_out = BaseName()
