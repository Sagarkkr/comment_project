from django.contrib.auth import get_user_model
from rest_framework import serializers
from comment_handle.models import Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',"is_superuser","username","email","first_name"]


class CommentSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id','user','created_at', 'is_flagged', 'flagged_reason','text']