#       FOR Web API :: 
# SERIALIZING and DESERIALIZING snippet instances into 
# REPRESENTATIONS such as JSON. 
# We can do this by declaring serializers that work
# similar to Django's forms. 
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

"""
SERIALIZER class is similar to a Django FORM class
similar VALIDATION FLAGS on fields, 
such as required, max_length and default.
"""


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # #                          🪆       ⬇️ controlling how the browsable API should be displayed,
    # code = serializers.CharField(style={'base_template': 'textarea.html'})#🫧= widget = widgets.Textarea on django FORM CLASS 
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#   CREATE() and UPDATE() methods  --- 
#   define how FULLY FLEDGED INSTANCES are CREATED or MODIFIED 
#   when calling serializer.save()
#
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)


    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance