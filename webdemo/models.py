from django.db import models

class Chat(models.Model):
    chat = models.TextField()

    def summarize(self):
        pass