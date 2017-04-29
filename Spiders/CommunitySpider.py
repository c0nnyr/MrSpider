# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
import GlobalMethod as M
from BaseItem import BaseItem
from sqlalchemy import Column, Text, DateTime

_engine, _session, _Model = M.create_db_engine('community')
class CommunityItem(BaseItem, _Model):
	__tablename__ = 'community'
	db = _session

	_crawl_date = Column(DateTime())
	meta_district = Column(Text(), primary_key=True)
	meta_price_level = Column(Text(), primary_key=True)
	meta_start_url = Column(Text())

	url = Column(Text(), primary_key=True)
	community_id = Column(Text())

	title = Column(Text())
	district = Column(Text())
	bizcircle = Column(Text())
	year_built = Column(Text())
	tag = Column(Text())

	def __str__(self):
		return '<{}> {} {}'.format(self.__class__.__name__, self.meta_start_url, self.url)
	__repr__ = __str__

class CommunityStateItem(BaseItem, _Model):
	__tablename__ = 'community_state'
	db = _session

	meta_start_date = Column(Text(), primary_key=True)
	meta_district = Column(Text(), primary_key=True)
	meta_price_level = Column(Text(), primary_key=True)
	url = Column(Text(), primary_key=True)

	sale_info = Column(Text())
	rent_info = Column(Text())
	unit_price = Column(Text())
	on_sale_count = Column(Text())

	def __str__(self):
		return '<{}> {}'.format(self.__class__.__name__, self.url)
	__repr__ = __str__

_Model.metadata.create_all(_engine)#类型建立后,才能这样建立表
class CommunitySpider(BaseLianjiaSpider):
	VALIDATE_XPATH = '/html/body/div[4]/div[contains(@class,"leftContent")]'

	BASE_URL_CD = 'http://cd.lianjia.com/xiaoqu/{district}/{page}p{price_level}/'
	DISTRICTS_CD = [ 'jinjiang', 'qingyang', 'wuhou', 'gaoxing7', 'chenghua', 'jinniu', \
					 'gaoxinxi1', 'pidou', 'tianfuxinqu', 'shuangliu', 'wenjiang', \
					 'longquanyi', 'xindou',]

	PRICE_LEVELS_CD = [
		4,#1~1.5
		5,#1.5~2
		3,#0.8~1
		2,#0.5~0.8
		1,#<0.5
		6,#>2
	]

	def __init__(self, city='cd'):
		super(CommunitySpider, self).__init__()
		if city == 'cd':
			self.metas = [{'price_level':price_level, 'district':district} for price_level in self.PRICE_LEVELS_CD for district in self.DISTRICTS_CD]
			self.BASE_URL = self.BASE_URL_CD
		self.start_urls = M.fill_meta_extract_start_urls(self.BASE_URL_CD, self.metas)

	def parse(self, response):
		attr_map = {
			#attr xpath, re_filter
			'url':dict(xpath='a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'community_id':dict(xpath='a/@href', re_filter=r'xiaoqu/(?P<extract>\S+)/'),
			'title':dict(xpath='div[contains(@class, "info")]/div[contains(@class, "title")]/a/text()',),
			'district':dict(xpath='div[contains(@class, "info")]/div[contains(@class, "positionInfo")]/a[contains(@class, "district")]/text()',),
			'bizcircle':dict(xpath='div[contains(@class, "info")]/div[contains(@class, "positionInfo")]/a[contains(@class, "bizcircle")]/text()',),
			'year_built':dict(xpath='div[contains(@class, "info")]/div[contains(@class, "positionInfo")]/text()',),
			'tag':dict(xpath='div[contains(@class, "info")]/div[contains(@class, "tagList")]/span/text()',),
		}
		for item in self._parse_multipage(response, CommunityItem, '/html/body/div[4]/div[1]/ul/li', attr_map, '/html/body/div[4]/div[1]/div[2]/h2/span/text()', ('district', 'price_level', 'start_url')):
			yield item

		attr_map = {
			'url':dict(xpath='a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'sale_info':dict(xpath='div[contains(@class, "info")]/div[contains(@class, "houseInfo")]/a[1]/text()',),
			'rent_info':dict(xpath='div[contains(@class, "info")]/div[contains(@class, "houseInfo")]/a[2]/text()',),
			'unit_price':dict(xpath='div[contains(@class, "xiaoquListItemRight")]/div[contains(@class, "xiaoquListItemPrice")]/div[contains(@class, "totalPrice")]/span/text()',),
			'on_sale_count':dict(xpath='div[contains(@class, "xiaoquListItemRight")]/div[contains(@class, "xiaoquListItemSellCount")]/a/span/text()',),
		}

		for item in self._parse_items(response, '/html/body/div[4]/div[1]/ul/li', attr_map, CommunityStateItem, \
									  ('district', 'price_level', 'start_date')):
			yield item

