from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # Dynamic permission assignment based on the action (e.g., 'create' or 'list')
    def get_permissions(self):
        if self.action == 'create':
            # Allow anyone to create a comment
            return [AllowAny()]
        # Require authentication for other actions (list, retrieve, update, etc.)
        return [IsAuthenticated()]

    # Automatically set status to 'processed' when creating a new comment
    def perform_create(self, serializer):
        serializer.save(status='processed')
