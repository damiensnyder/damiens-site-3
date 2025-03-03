from django.db import models
from accounts.models import User


class Flag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200, unique=True)
    width = models.IntegerField()
    height = models.IntegerField()
    source = models.CharField(max_length=200)
    total_score = models.IntegerField(default=0)
    num_votes = models.IntegerField(default=0)
    leaderboard_score = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.leaderboard_score = self.total_score / (self.num_votes + 2)
        models.Model.save(self)

    def __str__(self) -> str:
        return self.name
    

class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    matchup_id = models.UUIDField()
    flag = models.ForeignKey(Flag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.IntegerField()

    def save(self, *args, **kwargs):
        models.Model.save(self)

    def __str__(self) -> str:
        return f"{self.matchup_id}: {self.flag.name} - {self.score} ({self.user})"