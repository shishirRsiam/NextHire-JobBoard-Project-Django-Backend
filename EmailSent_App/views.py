from rest_framework.response import Response
from rest_framework.views import APIView
from .email_sent import *
from Authentication_App.serializers import SimpleUserSerializer
from django.contrib.auth.models import User
class EmailSentView(APIView):
    def get(self, request):
        email_sent = request.GET.get('email_sent', None)
        if email_sent == 'reset_password':
            sent_password_reset_email(request, request.user)
        
        # http://localhost:8000/api/email/sent/?email_sent=forget_password&&email=shishir.siam01@gmail.com
        if email_sent == 'forget_password':
            print('($)'*30)
            email = request.GET.get('email', None)
            user = User.objects.filter(email=email).first()

            print('email', email, 'user', user)
            if not user:
                return Response({'error': 'User not found!'}, status=404)
            sent_forget_password_email(request, user)
            return Response({'message': 'Email sent successfully!'}, status=200)
        
        user = SimpleUserSerializer(request.user)
        return Response({"user": user.data})
