# coding:utf-8
import cPickle
class Request(object):

	def __init__(self, url, method='get', data=None, meta=None, callback=None, cache_valid_duration=10, **kwargs):
		self._url = url
		self._data = data or {}
		self._meta = meta or {}
		self._method = method
		self._callback = callback

	@property
	def url(self):
		return self._url
	@property
	def data(self):
		return self._data
	@property
	def meta(self):
		return self._meta
	@property
	def method(self):
		return self._method
	@property
	def callback(self):
		return self._callback

	def dumps(self):
		return cPickle.dumps(dict(url=self.url, data=self.data, meta=self.meta, method=self.method))

	@classmethod
	def loads(cls, s):
		if isinstance(s, unicode):
			s = s.encode('utf-8')
		dct = cPickle.loads(s)
		return cls(**dct)

	def __str__(self):
		return '<Request {} {} {}>'.format(self._url, self._data, self._meta)
	__repr__ = __str__

class RequestImg(Request):
	def __init__(self, *args, **kwargs):
		if 'callback' not in kwargs:
			kwargs['callback'] = '_parse_img'
		super(RequestImg, self).__init__(*args, **kwargs)
