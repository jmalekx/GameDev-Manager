from django.db import models

class Developer(models.Model):
    """Represents game developer with personal and professional info"""
    name = models.CharField(max_length=100)
    about = models.TextField()
    experience_years = models.IntegerField()
    available_to_hire = models.BooleanField(default=True)
    join_date = models.DateField()

    def __str__(self):
        """Return name of developer"""
        return self.name
    
    def as_dict(self):
        """Return dictionary representation of developer"""
        return{
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'experience_years': self.experience_years,
            'available_to_hire': self.available_to_hire,
            'join_date':self.join_date,
        }
    
class Game(models.Model):
    """Represents game with relevant details and associated developers"""
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


    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'release_date': self.release_date,
            'platform': self.platform, 
            'platform_display': self.get_platform_display(),  #human readable version
            'developers': [
                {
                    'developer_id': gd.developer.id,
                    'developer_name': gd.developer.name,
                    'role': gd.role,
                    'assigned_on': gd.assigned_on
                }
                for gd in self.gamedeveloper_set.all()
            ]
        }

class GameDeveloper(models.Model):
    """Associates game with developer and role"""
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
        
