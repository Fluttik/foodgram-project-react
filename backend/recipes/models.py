from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
MAX_CHAR_LENGTH = 200


class Tag(models.Model):
    """Модель тэгов."""
    name = models.CharField(
        verbose_name='название тэга',
        max_length=MAX_CHAR_LENGTH,
        unique=True
    )
    color = models.CharField(
        verbose_name='цвет в hex формате',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.slug


class Ingredient(models.Model):
    """Модель ингридиентов."""
    name = models.CharField(
        verbose_name='название ингридиента',
        max_length=MAX_CHAR_LENGTH
    )
    measurement_unit = models.CharField(
        verbose_name='единица измерения',
        max_length=MAX_CHAR_LENGTH
    )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        related_name='recipe',
        verbose_name='автор рецепта',
        on_delete=models.CASCADE,
        # db_index=True,
    )
    name = models.CharField(
        verbose_name='название рецепта',
        max_length=MAX_CHAR_LENGTH,
        # db_index=True
    )
    image = models.ImageField(
        verbose_name='картинка рецепта',
        upload_to='recipes/image/'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='текст рецепта',)
    tags = models.ManyToManyField('Tag', related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='время приготовления'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
    )

    class Meta:
        ordering = ('-pub_date',)


class RecipeIngredient(models.Model):
    """Модель для связи рецептов с их ингредиентами."""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='r_i',
        verbose_name='рецепт',
        help_text='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
        help_text='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='Уникальный ингридиент в рецепте'),
        )
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'ингредиенты в рецепте'

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} – {self.amount}'


class Favorite(models.Model):
    """Модель для избранных рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='избранный рецепт'
    )

    class Meta:
        verbose_name = 'избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorites',
            ),
        )


class ShoppingBasket(models.Model):
    """Модель для списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_basket'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        )
