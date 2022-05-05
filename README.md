# DJANGO REST_FRAMEWORK
URL::  https://www.django-rest-framework.org

# Tutorial 1: Serialization
   ## ----------------------🍄  WORKING WITH SERIALIZERS  🍄------------------
SERIALIZER class is similar to a Django FORM class 

both use similar VALIDATION FLAGS on fields such as::
         required, max_length and default.   
 ```python 
 from rest_framework import serializers
 
 
            class SnippetSerializer(serializers.ModelSerializer):
                   title = serializers.CharField(required=False, default='friendly', max_length=100)
 ```
 
📟 IN Terminal📟: 
```python
python manage.py shell   🪬 exit()

>>from snippets.models import Snippet

>>from snippets.serializers import SnippetSerializer

>>from rest_framework.renderers import JSONRenderer

>>from rest_framework.parsers import JSONParser
```

---
###                🩻 SERIALIZING DATA 🩻

#### 1️⃣ CODE SNIPPETS::
```python
SNIPPET = Snippet(code='foo = "bar"\n')
SNIPPET.save()

SNIPPET = Snippet(code='print("hello, world")\n')
SNIPPET.save()
```
#### 2️⃣ SERIALIZING SNIPPETS:: (Python Native Datatypes)
```python
SERIALIZER = SnippetSerializer(SNIPPET)

SERIALIZER.data 
```
>{'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}

#### 3️⃣ RENDER INTO JSON:: (finalize serialization proccess)
```python

content = JSONRenderer().render(SERIALIZER.data)

content 
```
>b'{"id": 2, "title": "", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'

---
###              🩻  DESERIALIZING DATA 🩻

#### 1️⃣ PARSE STREAM INTO PYTHON NATIVE DATATYPES::
```python
import io

stream = io.BytesIO(content)

data = JSONParser().parse(stream)
```
#### 2️⃣ RESTORE NATIVE DATATYPES TO FULLY POPULATED OBJECT INSTANCE 
```python
SERIALIZER = SnippetSerializer(data=data)

SERIALIZER.is_valid()
```
       True
```python                 
SERIALIZER.validated_data
```
>OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
```python
SERIALIZER.save()
```
> <Snippet: Snippet object>

###      SERIALIZE QUERYSETS INSTEAD OF MODEL INSTANCES       ⬇️ ⬇️
```python
SERIALIZER = SnippetSerializer(Snippet.objects.all(), many=True)

SERIALIZER.data
```
>[OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]

# Tutorial 2: Requests and Responses
