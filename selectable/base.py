from django.utils.encoding import smart_unicode


class LookupBase(object):

    def _name(cls):
        app_name = cls.__module__.split('.')[-2].lower()
        class_name = cls.__name__.lower()
        name = u'%s-%s' % (app_name, class_name)       
        return name
    name = classmethod(_name)

    def get_query(self, request):
        return []

    def format_item(self, item):
        return smart_unicode(item)

