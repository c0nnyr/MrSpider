# coding:utf-8
class BaseItem(object):
	def __init__(self, **kwargs):
		super(BaseItem, self).__init__()
		for k, v in kwargs.iteritems():
			setattr(self, k, v)

	def check_existence(self):
		return False
