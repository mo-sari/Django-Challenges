from django.db import models


class Question(models.Model):
    """Question Class"""
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()

    def __str__(self):
        return f'{self.title}'


class Choice(models.Model):
    """choice Class"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return f'Choice id: {self.pk}, {self.choice_text}'
