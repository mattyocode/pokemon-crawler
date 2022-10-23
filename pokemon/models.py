from django.db import models


class Ability(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

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
        return self.name.replace("-", " ")

    @property
    def stats_list(self):
        if len(self.stats) > 0:
            stats_list = []
            for stat in self.stats:
                try:
                    stats_list.append(f'{stat["stat"]["name"]}: {stat["base_stat"]}')
                except KeyError:
                    pass
            return stats_list
