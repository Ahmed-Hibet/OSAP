from django.db import models


class Message(models.Model):
    sender = models.ForeignKey("access.User", related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey("access.User", related_name='receiver', on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return 'From %s To %s' % (self.sender.username, self.receiver.username)
    