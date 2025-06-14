from .Authentication_App_Import import *
from JobPost_App.serializers import *
from Category_App.serializers import *
from Authentication_App.serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserRegistrationApiView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        print('\n\n' ,'()'*30)
        print(request.data)
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        role = request.data.get('role')
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        
        user = User.objects.filter(username=username).first()
        if user:
            response = get_username_or_email_already_exists_response('username')
            return Response(data=response, status=400)

        user = User.objects.filter(email=email).first()
        if user:
            response = get_username_or_email_already_exists_response('email')
            return Response(data=response, status=400)
        
        user = User.objects.create_user(
            first_name=first_name, last_name=last_name,
            username=username, password=password,
            email=email, is_active=False,
        )
        user_profile = UserProfile.objects.create(user=user, role=role)
        user.save()
        user_profile.save()

        email_sent.sent_account_registration_activation_email(request, user)

        response = get_successful_account_registration_response()
        return Response(data=response, status=201)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        print('()'*30)
        print(request.data)
        
        return Response({"message": "User updated successfully."})

class LoginApiView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_active:
                response = get_account_not_active_response()
                return Response(response, status=400)

            token, _ = Token.objects.get_or_create(user=user) 
            response = get_successful_login_response(user, token)
            return Response(response, status=200)
        
        response = get_failed_login_response()
        return Response(response, status=400)
    
class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, idb64, token):
        id = urlsafe_base64_decode(idb64).decode()
        user = User.objects.get(id=id)
        if user:
            if user.is_active:
                response = get_already_account_activation_response()
                return Response(response, status=200)
            
            else:
                user.is_active = True
                user.save()

                login(request, user)
                
                response = get_successful_account_activation_response()
                return Response(response, status=200)

        response = get_failed_account_activation_response()
        return Response(response, status=400)
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            logout(request)
            return Response({"message": "Logged out successfully."})
        except Token.DoesNotExist:
            return Response({"error": "Token not found."})
        
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        appliedJobs = user.applied.all().order_by('-id')
        postedJob = user.jobposts.all().order_by('-id')

        userSerializer = UserSerializer(user.userprofile)
        jobPostSerializer = JobPostSerializer(postedJob, many=True)
        AppliedSerializer = ApplySerializer(appliedJobs, many=True)
        response = {
            "userData": userSerializer.data,
            "appliedData": AppliedSerializer.data,
            "postedData": jobPostSerializer.data,
        }
        return Response(response)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        can_post = request.query_params.get('can_post', None)
        if can_post:
            return Response(
                {"can_post": request.user.userprofile.role == 'Employer'},
            )
        userSerializer = UserSerializer(user.userprofile)
        response = {
            "userData": userSerializer.data,
        }
        return Response(response)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        print('()'*30)
        return Response({"message": "User updated successfully."})
    

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print('()'*30)
        print(request.data)
        if request.data['resone'] == 'userProfile':
            userprofile = request.user.userprofile
            userprofile.bio = request.data.get('bio')
            userprofile.resume = request.data.get('resume')
            userprofile.skill.set(request.data.get('skill'))
            userprofile.save()
        elif request.data['resone'] == 'user':
            user = request.user
            user.username = request.data.get('username')
            user.first_name = request.data.get('first_name')
            user.last_name = request.data.get('last_name')
            user.save()
            print(user)
        return Response({"message": "User updated successfully."})





from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

class UpdatePasswordView(APIView):
    def post(self, request, *args, **kwargs):
        print('(^)'*30)
        print(request.data)
        token = request.data.get('token')
        password = request.data.get('password')
        id = urlsafe_base64_decode(request.data.get('uid'))
        
        if not id or not token or not password:
            return Response({"error": "Missing required fields."}, status=400)

        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid token."}, status=400)

        user.password = make_password(password)
        user.save()

        return Response({"message": "Password updated successfully."})
    

