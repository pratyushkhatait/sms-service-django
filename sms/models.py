from django.db import models


class Account(models.Model):
    auth_id = models.CharField(max_length=40, blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account'

    def __str__(self):
        return str(self.username)


class PhoneNumber(models.Model):
    number = models.CharField(max_length=40, blank=True, null=True)
    account = models.ForeignKey(Account, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'phone_number'

    def __str__(self):
        return str(self.number)

