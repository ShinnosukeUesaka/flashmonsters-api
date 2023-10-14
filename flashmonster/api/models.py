from django.db import models

# Create your models here.


class AppUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, unique=True)

class Word(models.Model):
    monster_image = models.CharField(max_length=200)
    monster_description = models.CharField(max_length=500)
    generated = models.BooleanField(default=False)
    learning= models.BooleanField(default=True)

    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='words')

class Examples(models.Model):
    example_sentence = models.CharField(max_length=500)
    image = models.CharField(max_length=200)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='examples')
