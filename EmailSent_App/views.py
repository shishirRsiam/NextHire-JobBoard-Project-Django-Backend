from rest_framework.response import Response
from rest_framework.views import APIView
from .email_sent import *
from Authentication_App.serializers import SimpleUserSerializer

class EmailSentView(APIView):
    def get(self, request):
        email_sent = request.GET.get('email_sent', None)
        if email_sent == 'reset_password':
            sent_password_reset_email(request.user)
        
        user = SimpleUserSerializer(request.user)
        return Response({"user": user.data})
