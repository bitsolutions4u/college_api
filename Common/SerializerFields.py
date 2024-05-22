from rest_framework import serializers



class FileRelatedField(serializers.RelatedField):
    """
    A read only field that represents its targets using their
    plain string representation.
    """

    def __init__(self, **kwargs):
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def to_representation(self, value):
        # return self.context['request'].build_absolute_uri(value.url)
        # # return str(value)
        try:
            url = value.url
            res =self.context['request'].build_absolute_uri(url)

        except Exception as e:
            url = "static/images/thumbnail/default_no_file.png"
            res =self.context['request'].build_absolute_uri(url)


        # res =self.context['request'].build_absolute_uri(url)
        
        return res


class FileThumbnailRelatedField(serializers.RelatedField):
    """
    A read only field that represents its targets using their
    plain string representation.
    """

    def __init__(self, **kwargs):
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def to_representation(self, value):

        try:
            url = value.url
            res =self.context['request'].build_absolute_uri(url)

        except Exception as e:
            url = "static/images/thumbnail/default_no_file.png"
            res =self.context['request'].build_absolute_uri(url)


        # res =self.context['request'].build_absolute_uri(url)
        
        return res