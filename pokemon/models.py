from django.db import models


class Ability(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Ability: {self.name}"

    class Meta:
        verbose_name = "abilities"


class Pokemon(models.Model):
    name = models.CharField(max_length=100, unique=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    stats = models.JSONField(null=True)
    sprite = models.URLField(null=True)
    abilities = models.ManyToManyField(to=Ability, related_name="pokemon")

    def __str__(self):
        return self.name
