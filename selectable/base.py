from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode


class LookupBase(object):

    def _name(cls):
        app_name = cls.__module__.split('.')[-2].lower()
        class_name = cls.__name__.lower()
        name = u'%s-%s' % (app_name, class_name)       
        return name
    name = classmethod(_name)

    def _url(cls):
        return reverse('selectable-lookup', args=[cls.name()])
    url = classmethod(_url)

    def get_query(self, request):
        return []

    def get_item_label(self, item):
        return smart_unicode(item)

    def get_item_id(self, item):
        return smart_unicode(item)

    def get_item_value(self, item):
        return smart_unicode(item)

    def get_item(self, value):
        return []

    def format_item(self, item):
         return {
            'id': self.get_item_id(item),
            'value': self.get_item_value(item),
            'label': self.get_item_label(item)
        }


