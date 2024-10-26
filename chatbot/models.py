from django.db import models

class ChatMessage(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    message = models.TextField()
    is_agent_response = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatMessage (ID: {self.id}) at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']
