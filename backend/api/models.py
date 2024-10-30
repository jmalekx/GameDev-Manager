from django.db import models

class Developer(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    experience_years = models.IntegerField()
    available_to_hire = models.BooleanField(default=True)
    join_date = models.DateField()

    def __str__(self):
        return self.name
    
    def as_dict(self):
        return{
            'name': self.name,
            'about': self.about,
            'experience_years': self.experience_years,
            'available_to_hire': self.available_to_hire,
            'join_date':self.join_date,
        }
    
class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    developer = models.ManyToManyField(Developer, through = 'GameDeveloper')

    PC = 'PC'
    CONSOLE = 'Console'
    MOBILE = 'Mobile'

    PLATFORM_TYPE = [
        (PC, 'Computer/Laptop'),
        (CONSOLE, 'Console'),
        (MOBILE, 'Android/iOS'),
    ]

    platform = models.CharField(
        max_length=7,
        choices=PLATFORM_TYPE,
        default=PC,
    )

    def __str__(self):
        return f"{self.title} ({self.get_platform_display()})"

class GameDeveloper(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer,on_delete=models.CASCADE)

    LEVEL_DESIGNER = 'Level Designer'
    PROGRAMMER = 'Programmer'
    ARTIST = 'Artist'
    ANIMATOR = 'Animator'
    SOUND_DESIGNER = 'Sound Designer'
    PROJECT_MANAGER = 'Project Manager'
    UI_UX_DESIGNER = 'UI/UX Designer'

    ROLE_CHOICES = [
        (LEVEL_DESIGNER, 'Level Designer'),
        (PROGRAMMER, 'Programmer'),
        (ARTIST, 'Artist'),
        (ANIMATOR, 'Animator'),
        (SOUND_DESIGNER, 'Sound Designer'),
        (PROJECT_MANAGER, 'Project Manager'),
        (UI_UX_DESIGNER, 'UI/UX Designer'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    assigned_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.developer.name} - {self.game.title} ({self.role})"
