from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        default_related_name = 'author'


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        default_related_name = 'publisher'


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        default_related_name = 'book'

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('annotations:book-details', args=[str(self.id)])


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        default_related_name = 'store'
