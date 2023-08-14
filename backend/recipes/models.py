from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название Тэга',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет в hex формате',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class Ingridient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200
    )
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='recipes/'
    )
    text = models.TextField(verbose_name='Текст рецепта',)
    ingredients = ...
    tags = models.ManyToManyField('Tag', related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
