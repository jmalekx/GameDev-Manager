from django.db import models

class Developer(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    experience_years = models.IntegerField()
    available_to_hire = models.BooleanField(default=True)
    join_date = models.DateField()

    def __str__(self):
        return self.name
    
class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()

    PC = 'PC'
    Console = 'Console'
    Mobile = 'Mobile'
    PLATFORM_TYPE = [
        (PC, 'Computer/Laptop'),
        (Console, 'Console'),
        (Mobile, 'Android/iOS'),
    ]

    platform = models.CharField(
        max_length=7,
        choices=PLATFORM_TYPE,
        default=PC,
    )

    def __str__(self):
        return f"{self.title} ({self.get_platform_display()})"
