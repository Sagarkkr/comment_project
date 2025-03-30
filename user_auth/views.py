from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets,status,mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
#local imports
from user_auth.serializers import ChangePasswordSerializer,Logoutserializer,ResetPasswordSerializer,SignInSerializer

User = get_user_model()
class UserAuthViewset(viewsets.GenericViewSet,mixins.CreateModelMixin):
    """
        User auth viewset to handle users credentials
    """
    queryset = User.objects.all()
    serializer_class = SignInSerializer
    permission_classes = [AllowAny]


    @action(detail=False, methods=['PATCH'],permission_classes=[IsAuthenticated],serializer_class=ChangePasswordSerializer)
    def change_password(self, request, *args, **kwargs):
        '''
        This function is used for changing the current dashboard user password with some validations applied on serializers.
        '''
        try:
            # Retrieve the user instance
            user = self.request.user
            serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)

            # Validate if the old password and new password are the same
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['password']
            if check_password(old_password, user.password):
                if old_password == new_password:
                    return Response({'error': 'Old password and new password cannot be the same.'})
            else:
                return Response({'error': 'Old password is not correct.'})

            serializer.update(user, serializer.validated_data)
            return Response({'status': 'success', 'message': 'Password changed successfully.'})

        except Exception as e:
            error_message = str(e)
            if 'old_password' in error_message:
                return Response({'error': 'Old password is not correct.'}, status=status.HTTP_403_FORBIDDEN)
            elif 'password' in error_message:
                return Response({'error': f'Password fields did not match'}, status=status.HTTP_403_FORBIDDEN)
            elif 'len' in error_message:
                return Response({'error': 'Password must be at least 8 characters long.'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'error': f'An error occurred while changing the password {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'],permission_classes=[IsAuthenticated],serializer_class=ResetPasswordSerializer)
    def reset_password(self, request):
        '''
            Reset password to change password 
        '''
        try:
            user = self.request.user
            serializer = ResetPasswordSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.update(user, serializer.validated_data)
            return Response({'msg': 'Password Reset Successfully'})

        except Exception as e:
            error_message = str(e)
            if 'old_password' in error_message:
                return Response({'error': 'New password cannot be same as old password.'}, status=status.HTTP_403_FORBIDDEN)
            elif 'password' in error_message:
                return Response({'error': 'Password fields did not match'}, status=status.HTTP_403_FORBIDDEN)
            elif 'len' in error_message:
                return Response({'error': 'Password must be at least 8 characters long.'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'error': f'An error occurred while resetting the password. Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['POST'],permission_classes=[IsAuthenticated],serializer_class=Logoutserializer)
    def logout(self, request):
        '''
         Logout the user by deleting the token of user
        '''
        try:
            logout_serializer =Logoutserializer(data=request.data)
            logout_serializer.is_valid(raise_exception=True)
            token = Token.objects.get(key=logout_serializer.validated_data.get("refresh_token"))
            token.delete()
            return Response("user successfully logout")

        except Exception as e:
            return Response({'error': f'Logout failed. Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        