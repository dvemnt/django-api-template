# coding=utf-8


class SerializerViewMixin(object):

    def dispatch(self, *args, **kwargs):
        self.serializer_class = self.get_serializer_class()
        return super(SerializerViewMixin, self).dispatch(*args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_class
