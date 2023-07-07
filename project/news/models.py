from django.db import models
from django.core.validators import MinValueValidator


# Создаём модель товара
class News(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,  # названия новостей не должны повторяться
    )
    description = models.TextField()
    creationTime = models.DateTimeField(auto_now_add=True)
    authorNew = models.CharField(max_length=30)

    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news',  # все новости в категории будут доступны через поле news
    )


    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

#  создаём категорию, к которой будет привязываться новость
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # названия категорий тоже не должны повторяться

    def __str__(self):
        return f'{self.name.title()}'


from django.db import models

