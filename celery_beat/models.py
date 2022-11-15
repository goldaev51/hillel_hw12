from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, null=False)
    born_date = models.CharField(max_length=100)
    born_location = models.CharField(max_length=100)
    description = models.CharField(max_length=4000)

    def __str__(self):
        return self.name


class Tags(models.Model):
    text = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.text


class Quote(models.Model):
    text = models.CharField(max_length=200, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.text
