from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from webpages.models import OldQuestions
from .serializers import ItemSerializer
from rest_framework import status


@api_view(['GET'])
def get_data_simple(request): # this is simplized version
    test = {"name":"anything", "age":12}
    return Response(test)


@api_view(['GET'])
def get_data(request,name=None): # this is real data version
    items = OldQuestions.objects.filter(user__username=name) # in one to many relationships we always use filter not get
    serializer = ItemSerializer(items, many = True) # many =  True when we want to serialize more that one item and many = False when we serialize one item only
    return Response(serializer.data)

@api_view(['POST']) # works only when we work on a whole table with no
def add_data_simple(request): # this is simplized version to add data to the api
    serializer = ItemSerializer(data = request.data) # this will get the data submitted with the request
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
    




@api_view(['POST'])
def add_data(request, name): 
    try:
        # Fetch the user object based on the username
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Create a dictionary from the request data and add the user to it
    data = request.data.copy() # data is a mirror to the oldquestions table as we used this model to create the serializer class
    data['user'] = user.id  # Assign the user to the data 
    
    serializer = ItemSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()  # This will save the new question-answer pair with the specified user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
