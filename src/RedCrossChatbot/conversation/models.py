from django.db import models


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user


class ConversationLine(models.Model):
    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='lines')
    author = models.CharField(max_length=100, choices=[('user', 'User'), ('bot', 'Bot')])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}: {self.text}'
