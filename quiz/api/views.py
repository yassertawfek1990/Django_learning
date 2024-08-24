from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from webpages.models import OldQuestions
from .serializers import ItemSerializer
from rest_framework import status
from django.shortcuts import render


# @api_view(['GET'])
# def get_data_simple(request): # this is simplized version
#     test = {"name":"anything", "age":12}
#     return Response(test)

# API view to get quiz data for a specific user
@api_view(['GET'])
def get_data(request, name=None):
    items = OldQuestions.objects.filter(user__username=name)  # Filter OldQuestions based on the username
    serializer = ItemSerializer(items, many=True)  # Serialize the queryset (many=True since there are multiple items)
    return Response(serializer.data)  # Return the serialized data as a JSON response


# @api_view(['POST']) # works only when we work on a whole table with no
# def add_data_simple(request): # this is simplized version to add data to the api
#     serializer = ItemSerializer(data = request.data) # this will get the data submitted with the request
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)



# API view to add quiz data for a specific user
@api_view(['POST'])
def add_data(request, name): 
    try:
        # Fetch the User object based on the username
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)  # Return an error if the user does not exist
    
    # Create a dictionary from the request data and add the user to it
    data = request.data.copy()  # Create a copy of the request data
    data['user'] = user.id  # Assign the user's ID to the data
    
    serializer = ItemSerializer(data=data)  # Initialize the serializer with the modified data
    
    if serializer.is_valid():
        serializer.save()  # Save the new question-answer pair to the database
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the serialized data with a 201 Created status
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors with a 400 Bad Request status

# View to render the API documentation page
def doc(request):
    return render(request, "api/docs.html")  # Render an HTML page for the API documentation


    
