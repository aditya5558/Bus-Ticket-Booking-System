from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MaxLengthValidator,MaxValueValidator,MinValueValidator
# Create your models here.

class User(AbstractUser):
    is_passenger = models.BooleanField(default=False)
    is_bus_operator = models.BooleanField(default=False)

    def __str__(self):
        return("Username : " + self.username + " Passenger : " + str(self.is_passenger) + " Bus Operator  : " + str(self.is_bus_operator))


class UserFeedback(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=300,blank=False)
    comment = models.TextField(blank=True)
    rating = models.IntegerField(blank=True,choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')))

    def __str__(self):
        return("Username : " + self.user.username + " Rating : " + str(self.rating))

class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0,blank=False)
    # four_digit_pin = models.IntegerField(unique=True,blank=False,validators=[MaxLengthValidator(4),MinLengthValidator(4)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return("Username : " + self.user.username + " Balance : " + str(self.balance))


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    type = models.CharField(blank=False,max_length=10,choices=(('Credit','Credit'),('Debit','Debit')))
    old_balance = models.FloatField(blank=False)
    new_balance = models.FloatField(blank=False)
    trans_amt = models.FloatField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return("Username : " + self.wallet.user.username + " Type : " + str(self.type) + " Transaction Amount : " + str(self.trans_amt))

class Bus(models.Model):
    bus_op = models.ForeignKey(User,on_delete=models.CASCADE)
    bus_type = models.CharField(max_length=10,choices=(('AC','AC'),('Non-AC','Non-AC')))
    # date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    source = models.CharField(max_length=30,blank=True)
    destination = models.CharField(max_length=30,blank=True)
    journey_duration = models.TimeField(blank=True)
    rating = models.IntegerField(null=True,blank=True,choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')))
    price = models.FloatField(blank=False)

    def __str__(self):
        return("Bus Operator : " + str(self.bus_op.username) + " Type : " + str(self.bus_type) + " Price : " + str(self.price))

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True)
    wallet_initial = models.FloatField(blank=False)
    wallet_final = models.FloatField(blank=False)
    total_price = models.FloatField(blank=False)
    booking_id = models.CharField(unique=True,max_length=10,validators=[MaxLengthValidator(10),MinLengthValidator(10)])
    timestamp = models.DateTimeField(auto_now_add=True)
    num_tickets = models.IntegerField(blank=False)
    status = models.CharField(max_length=10,choices=(('Success','Success'),('Failed','Failed')))

    def __str__(self):
        return("Booking ID : " + str(self.booking_id) + " Total Price : " + str(self.total_price) + " Status : " + str(self.status))





