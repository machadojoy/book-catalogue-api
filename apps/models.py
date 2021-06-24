from django.db import models

class Author(models.Model):
    first_name = models.CharField(verbose_name="first name", max_length=255, help_text="Author's first name")
    last_name = models.CharField(verbose_name="last name", max_length=255, help_text="Author's last name")
    date_of_birth = models.DateField(verbose_name='date of birth', blank=True, null=True, help_text="Date of birth")
    date_of_death = models.DateField(verbose_name='date of death', blank=True, null=True, help_text="Date of death")

    class Meta:
        db_table = 'authors'
        ordering = ['date_of_birth']

    def __str__(self):
        return self.first_name + " " +self.last_name

class Language(models.Model):
    name = models.CharField(verbose_name="name", unique=True, max_length=255, help_text="Languages. eg: English")

    class Meta:
        db_table = 'languages'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name="name", unique=True, max_length=255, help_text="Book Genre")

    class Meta:
        db_table = 'genres'
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(verbose_name="title", max_length=255, help_text="Book title")
    author = models.ForeignKey('Author', related_name='author', on_delete=models.CASCADE)
    summary = models.TextField(verbose_name="summary",help_text="Book summary")
    isbn = models.CharField(verbose_name="isbn",max_length=13, unique=True,  help_text="ISBN")
    genre = models.ManyToManyField('Genre', help_text="Genre")
    language = models.ForeignKey('Language', related_name='language', on_delete=models.DO_NOTHING)
    price = models.IntegerField()
    published_date = models.DateField(verbose_name='publication date', blank=True, null=True, help_text="Date of publication")

    class Meta:
        db_table = 'books'
        ordering = ['title']

    def __str__(self):
        return self.title