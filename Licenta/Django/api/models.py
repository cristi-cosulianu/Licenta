from django.db import models

# Create your models here.

class Persons(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Payments(models.Model):
    payer = models.ForeignKey(Persons, on_delete = models.CASCADE)
    product = models.CharField(default="", max_length = 255, blank=True)
    price = models.FloatField(default=0.0, blank=True)

class PaymentsStatus(models.Model):
    payment = models.ForeignKey(Payments, on_delete = models.CASCADE)
    status = models.CharField(default="", max_length = 20, blank=True)
    reason = models.CharField(default="", max_length = 255, blank=True)

class Bills(models.Model):
    initiator = models.ForeignKey(Persons, on_delete = models.CASCADE)
    title = models.CharField(default="", max_length = 200, blank=True)
    date = models.DateTimeField()

class BillsToPayments(models.Model):
    bill = models.ForeignKey(Bills, on_delete = models.CASCADE)
    payment = models.ForeignKey(Payments, on_delete = models.CASCADE)

