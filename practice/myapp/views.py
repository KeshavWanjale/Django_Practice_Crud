from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json


def greet(request):
    """
    Description: 
        A simple view to return a greeting message.
    Parameter:
        request (HttpRequest): The HTTP request object.
    Returns: 
        HttpResponse: A plain text response containing "Greetings".
    """
    return HttpResponse("Greetings")

@csrf_exempt
def user_crud(request, user_id=None):
    """
    Description:
        A single function to handle all CRUD operations: Create, Read, Update, and Delete for User.
    Parameter:
        request (HttpRequest): The HTTP request object.
        user_id (int, optional): The ID of the user for operations like Update, Read (single user), and Delete.
    Returns:
        JsonResponse: A JSON response based on the operation performed (Success or Error message).
    """
    
    # GET method: Retrieve either all users or a single user if user_id is provided
    if request.method == 'GET':
        if user_id:  # Retrieve a specific user by ID
            try:
                user = User.objects.get(id=user_id)
                return JsonResponse({'id': user.id, 'name': user.name, 'age': user.age}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:  # Retrieve all users
            users = User.objects.all().values('id', 'name', 'age')
            users_list = list(users)  # Convert QuerySet to list of dicts
            return JsonResponse(users_list, safe=False, status=200)

    # POST method: Create a new user
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            age = data.get('age')

            # Validate incoming data
            if not name or not isinstance(age, int):
                return JsonResponse({'error': 'Invalid data'}, status=400)

            # Create the new user
            user = User.objects.create(name=name, age=age)
            return JsonResponse({'id': user.id, 'name': user.name, 'age': user.age}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    # PUT method: Update an existing user by ID
    elif request.method == 'PUT' and user_id:
        try:
            user = User.objects.get(id=user_id)
            data = json.loads(request.body)
            name = data.get('name')
            age = data.get('age')

            # Validate incoming data
            if not name or not isinstance(age, int):
                return JsonResponse({'error': 'Invalid data'}, status=400)

            # Update user details
            user.name = name
            user.age = age
            user.save()

            return JsonResponse({'id': user.id, 'name': user.name, 'age': user.age}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    # DELETE method: Delete a user by ID
    elif request.method == 'DELETE' and user_id:
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': f"User with id {user_id} deleted successfully."}, status=200)
        
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    # If the method is not allowed
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# def get_users(request):
#     """
#     Description:
#         Retrieves all users from the database and returns them as a JSON response.
#     Parameter:
#         request (HttpRequest): The HTTP request object.
#     Returns:
#         JsonResponse: A JSON array containing user data (id, name, age).
#     """
#     if request.method == 'GET':
#         users = User.objects.all().values('id', 'name', 'age')  # Getting data directly as a list of dictionaries
#         users_list = list(users)  # Convert QuerySet to list
#         return JsonResponse(users_list, safe=False)  # safe=False allows returning lists in JSON


# @csrf_exempt  # Exempting CSRF for simplicity in API testing, remove in production
# def create_user(request):
#     """
#     Description:
#         Creates a new user using the data from the request body.
#     Parameter:
#         request (HttpRequest): The HTTP request object containing the user's data (name and age).
#     Returns:
#         JsonResponse: A JSON response containing the newly created user's data or error message.
#     """
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)  # Parse the incoming JSON data
#             name = data.get('name')
#             age = data.get('age')

#             # Validate incoming data
#             if not name or not isinstance(age, int):
#                 return JsonResponse({'error': 'Invalid data'}, status=400)

#             # Create the new user object
#             user = User.objects.create(name=name, age=age)
#             return JsonResponse({'id': user.id, 'name': user.name, 'age': user.age}, status=201)
        
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)


# @csrf_exempt
# def update_user(request, contact_id):
#     """
#     Description:
#         Updates an existing user based on the provided user_id and request body.
#     Parameter:
#         request (HttpRequest): The HTTP request object containing updated data (name and age).
#         user_id (int): The ID of the user to update.
#     Returns:
#         JsonResponse: A JSON response containing the updated user's data or an error message.
#     """
#     if request.method == 'PUT':
#         try:
#             user = User.objects.get(id=contact_id)  # Find the user by ID
#             data = json.loads(request.body)  # Parse incoming JSON data
#             name = data.get('name')
#             age = data.get('age')

#             # Validate incoming data
#             if not name or not isinstance(age, int):
#                 return JsonResponse({'error': 'Invalid data'}, status=400)

#             # Update user data
#             user.name = name
#             user.age = age
#             user.save()

#             # Return the updated user data
#             return JsonResponse({'id': user.id, 'name': user.name, 'age': user.age}, status=200)

#         except User.DoesNotExist:
#             return JsonResponse({'error': 'User not found'}, status=404)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)


# @csrf_exempt
# def delete_user(request, contact_id):
#     """
#     Description:
#         Deletes a user based on the provided contact_id.
#     Parameter:
#         request (HttpRequest): The HTTP request object.
#         contact_id (int): The ID of the user to delete.
#     Returns:
#         JsonResponse: A JSON response indicating success or failure of the deletion.
#     """
#     if request.method == 'DELETE':
#         try:
#             # Find the user by ID
#             user = User.objects.get(id=contact_id)
#             user.delete()
#             return JsonResponse({'message': f"User with id: {contact_id} deleted successfully."}, status=200)
        
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'User not found'}, status=404)
