from django.db import models


class Caller(models.Model):
    user_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.user_name


class CallDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    caller = models.ForeignKey(Caller, on_delete=models.CASCADE)
    callee = models.CharField(max_length=20, blank=False, null=False)
    date = models.CharField(max_length=20)
    duration = models.CharField(max_length=20)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return f"CDR - {self.date}: {self.caller} -> {self.callee}"


