from django.db import models

# Create your models here.

class Transaction(models.Model):
    STATUS_CHOICE = [('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancel', 'Cancel')]
    TYPE_CHOICE = [('Withdraw', 'Withdraw'), ('Deposit', 'Deposit')]
    user = models.ForeignKey("access.User", on_delete=models.CASCADE)
    amount = models.IntegerField()
    _type = models.CharField(max_length=50, choices=TYPE_CHOICE)
    payment_system = models.CharField(max_length=300)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default="Pending")
    uuid = models.CharField(max_length=200)

    def __str__(self):
        return '%s %s %s birr' % (self.user.username, self._type, self.amount)
    