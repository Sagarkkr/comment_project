from django.shortcuts import render
from rest_framework import viewsets,status,mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#local imports
from comment_handle.models import Comment
from comment_handle.serializers import CommentSerializers

class CommentHandleViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    """
        Comment handle viewset to handle comments and create instance in db
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticated]

    def create(self,request):
        """
            Create method to create comments instance
        """
        try:
            user = self.request.user
            text = request.data.get('text')
            comment = self.get_queryset().create(user=user,text=text)
            comment.check_text()
            if comment.is_flagged:
                return Response({"msg":"Your comment is accepted but it contains unwanted text",
                                 "text":comment.flagged_reason},status=status.HTTP_200_OK)
            return Response({"msg":"Thanks for commenting"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['POST'],detail=True)
    def mark_as_approved(self,request,pk):
        """
            Function to mark a comment as approved
        """
        try:
            user = self.request.user
            if not user.is_superuser:
                return Response({"msg":"You don't have permission to approve a comment"},
                                status=status.HTTP_401_UNAUTHORIZED)
            comment = self.get_object()
            comment.is_approved = True
            comment.save()
            return Response({"msg":f"{comment.text} marked as approved"})
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
