from django.db import models

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    membership_type = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ])
    join_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )

    def __str__(self):
        return self.name


class GymClass(models.Model):
    name = models.CharField(max_length=100)
    schedule = models.DateTimeField()
    members = models.ManyToManyField(
        Member,
        blank=True,
        related_name='classes'
    )

    def __str__(self):
        return self.name