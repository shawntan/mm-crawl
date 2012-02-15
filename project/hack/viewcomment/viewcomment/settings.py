# Scrapy settings for viewcomment project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'viewcomment'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['viewcomment.spiders']
NEWSPIDER_MODULE = 'viewcomment.spiders'
DEFAULT_ITEM_CLASS = 'viewcomment.items.ViewcommentItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

