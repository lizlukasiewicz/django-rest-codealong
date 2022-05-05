# Create your views here.
#rom django.http import HttpResponse, JsonResponse
#from django.views.decorators.csrf import csrf_exempt
#from rest_framework.parsers import JSONParser
from rest_framework import status 
from rest_framework.decorators import api_view#🪺
from rest_framework.response import Response#👾
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

"""     REQUEST OBJECTS::
REST framework uses Request object extends HttpRequest
                    -more flexible req parsing
        
HttpRequest 🤜🏻 request.POST  # 👉🏻  Only handles FORM data.  Only works for 'POST' method.
Request 🤜🏻 request.data     # 👉🏻  Handles ARBITRARY data.  Works for 'POST', 'PUT' and 'PATCH' methods.

        👾 RESPONSE OBJECTS::👾
REST framework uses Response object, type of TemplateResponse
                    - takes unrendered content and uses content negotiation to determine the correct content type to return to the client 

return Response(data)  # Renders to content type as requested by the client 

        🪺 API VIEWS 🪺
2 Wrappers to write API views:
    @api_view decorator for working with function based views.
    APIView class for working with class-based views.
"""


#@csrf_exempt
@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data) #JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) #JsonResponse(serializer.data, status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #JsonResponse(serializer.errors, status=400)

#@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) #HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data) #JsonResponse(serializer.data)

    elif request.method == 'PUT':
        #data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)#JsonResponse(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)#JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) #HttpResponse(status=204)