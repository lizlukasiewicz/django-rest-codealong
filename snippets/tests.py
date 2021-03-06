from django.test import TestCase

# Create your tests here.
"""
      π  WORKING WITH SERIALIZERS  π
π IN Terminalπ:   python manage.py shell   πͺ¬ exit()
"""
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

#                π©» SERIALIZING DATA π©»

# 1οΈβ£ CODE SNIPPETS::
SNIPPET = Snippet(code='foo = "bar"\n')
SNIPPET.save()

SNIPPET = Snippet(code='print("hello, world")\n')
SNIPPET.save()

#2οΈβ£ SERIALIZING SNIPPETS:: (Python Native Datatypes)
SERIALIZER = SnippetSerializer(SNIPPET)
SERIALIZER.data # π π 
                    #-> {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}

#3οΈβ£ RENDER INTO JSON:: (finalize serialization proccess)
content = JSONRenderer().render(SERIALIZER.data)
content #  π π 
            #-> b'{"id": 2, "title": "", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'


#               π©»  DESERIALIZING DATA π©»

# 1οΈβ£ PARSE STREAM INTO PYTHON NATIVE DATATYPES::
import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)

# 2οΈβ£ RESTORE NATIVE DATATYPES TO FULLY POPULATED OBJECT INSTANCE 
SERIALIZER = SnippetSerializer(data=data)
SERIALIZER.is_valid()
                # True
SERIALIZER.validated_data
                # OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
SERIALIZER.save()
                # <Snippet: Snippet object>

## SERIALIZE QUERYSETS INSTEAD OF MODEL INSTANCES       β¬οΈ β¬οΈ
SERIALIZER = SnippetSerializer(Snippet.objects.all(), many=True)
SERIALIZER.data
            # [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), 
            #       ('linenos', False), ('language', 'python'), ('style', 'friendly')]),
            #  OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), 
            #       ('linenos', False), ('language', 'python'), ('style', 'friendly')]), 
            #  OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), 
            #       ('linenos', False), ('language', 'python'), ('style', 'friendly')])]
