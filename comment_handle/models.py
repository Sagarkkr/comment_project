from django.contrib.auth import get_user_model
from django.db import models
from comment_handle.google_api import HandleText

User = get_user_model()

class BaseModel(models.Model):
    """
    Data model to save common data used in models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    """data created date and time."""

    modified_at = models.DateTimeField(auto_now=True)
    """data update date and time."""

    class Meta:
        abstract = True

class Comment(BaseModel):
    """
        Comment model to store comment of a user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """Field to store instance of user commented"""

    text = models.TextField()
    """Text field of actual comment"""

    is_flagged = models.BooleanField(default=False)
    """Is flagged to check if comment contains unwanted"""

    flagged_reason = models.TextField(blank=True, null=True)
    """Reason why comment is flagged"""

    is_approved = models.BooleanField(default=False)
    """Is approved to check if comment is approved or not"""

    def __str__(self):
        return self.text
    
    def check_text(self):
        """
            Check whether the text contains unusual words
        """
        nlp_response = (HandleText().call_google_api(self.text)).get("moderationCategories")
        resp_id = []
        resp_text = []
        for data in nlp_response:
            if data.get("confidence") >= 0.6:
                resp_id.append(data.get("confidence"))
                resp_text.append(data.get("name"))
        if resp_id:
            self.is_flagged = True
            self.flagged_reason = "This text contains " + ", ".join(map(str,resp_text))
        self.save()
        return self
