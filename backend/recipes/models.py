from django.db import models


class Ingredients(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    measurement_unit = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    color = models.CharField(max_length=7, null=False, blank=False)
    slug = models.CharField(max_length=200, unique=True, null=False, blank=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name
