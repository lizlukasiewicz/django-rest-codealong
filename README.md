# DJANGO REST_FRAMEWORK
URL::  https://www.django-rest-framework.org

---
---
# Tutorial 1: Serialization

   ## ----🍄  WORKING WITH SERIALIZERS  🍄----
SERIALIZER class is similar to a Django FORM class 

both use similar VALIDATION FLAGS on fields such as::
         required, max_length and default.   
 ```python 
 from rest_framework import serializers
 
 
            class SnippetSerializer(serializers.ModelSerializer):
                   title = serializers.CharField(required=False, default='friendly', max_length=100)
 ```
 
<<< 📟   IN PYTHON TERMINAL  📟 <<<
```python
python manage.py shell   🪬 exit()

>>from snippets.models import Snippet

>>from snippets.serializers import SnippetSerializer

>>from rest_framework.renderers import JSONRenderer

>>from rest_framework.parsers import JSONParser
```

---
##                SERIALIZING DATA 

#### 1️⃣ CODE SNIPPETS::
```python
>>SNIPPET = Snippet(code='foo = "bar"\n')
>>SNIPPET.save()

>>SNIPPET = Snippet(code='print("hello, world")\n')
>>SNIPPET.save()
```
#### 2️⃣ SERIALIZING SNIPPETS:: (Python Native Datatypes)
```python
>>SERIALIZER = SnippetSerializer(SNIPPET)

>>SERIALIZER.data 
```
>{'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}

#### 3️⃣ RENDER INTO JSON:: (finalize serialization proccess)
```python

>>content = JSONRenderer().render(SERIALIZER.data)

>>content 
```
>b'{"id": 2, "title": "", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'

---
##               DESERIALIZING DATA 

#### 1️⃣ PARSE STREAM INTO PYTHON NATIVE DATATYPES::
```python
>>import io

>>stream = io.BytesIO(content)

>>data = JSONParser().parse(stream)
```
#### 2️⃣ RESTORE NATIVE DATATYPES TO FULLY POPULATED OBJECT INSTANCE 
```python
>>SERIALIZER = SnippetSerializer(data=data)

>>SERIALIZER.is_valid()
```
>True
```python                 
>>SERIALIZER.validated_data
```
>OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
```python
>>SERIALIZER.save()
```
> <Snippet: Snippet object>

#### 3️⃣ SERIALIZE QUERYSETS INSTEAD OF MODEL INSTANCES
```python
>>SERIALIZER = SnippetSerializer(Snippet.objects.all(), many=True)

>>SERIALIZER.data
```
>[OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]

---
---
# Tutorial 2: Requests and Responses
🌅   IN `views.py` MODULE   🌅
## ---- Request objects ----

`Request` object extends regular `HttpRequest` BUT with more flexible parsing 
with `request.data` attribute (which is similar to `request.POST` but better with Web APIs)

```python
request.POST # only handles form data, only works for `POST` method

request.data # handles arbitrary data, works for `POST`, `PUT`, `PATCH` methods 
```
⋅⋅⋅  SO::
```python
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

def snippet_detail(request, pk):
   if request.method == 'GET':
      serializer = SnippetSerializer(snippet)
      return Response(serializer.data)#👈🏻
   
   elif request.method == 'PUT':
      serializer = SnippetSerializer(snippet, data=request.data)#👈🏻
      #if serializer.is_valid():
         #serializer.save()
         return Response(serializer.data)#👈🏻
      #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

```
## ---- Response objects ----

`Response` object is a type of `TemplateResponse` 
that takes unrendered content and uses content negotiation to determine the correct content type to return to the client.

```python
return Response(data) # Renders to content type as requested by the client
```
⋅⋅⋅ SO ::
```python
from rest_framework.response import Response

def some_function(request):
   #if request.method == 'whatever':
        #do_this = to + that
        return Response(serializer.data)
    #elif request.method == 'this_other_thing':
         # blah blah
         # some conditional :
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
## ---- Status Codes ----
```python
from rest_framework import status

   def snippet_list(request):
      if request.method == 'POST':
         # yadda yadda yadda
         return Response(serializer.data, status=status.HTTP_201_CREATED)#👈🏻 Status Code
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)#👈🏻
```

## ---- Wrapping API views ----
+ makes sure you recieve `Request` instances in your view,
+ adding context to `Response` objects for content negotiation
+ returns `405 Method Not Allowed` responses when appropriate
+ handles `ParseError` exceptions when accessing `request.data` with malformed input

`@api_view` = function based views.

`APIView` = class-based views
```python
from rest_framework.decorators import api_view, APIView

@api_view(['GET', 'POST']) 
         #or ::
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_list(request):

```
