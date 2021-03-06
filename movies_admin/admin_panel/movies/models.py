import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = 'content\".\"genre'

    def __str__(self):
        return self.name


class Person(TimeStampedMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    full_name = models.CharField(_('full_name'), max_length=255)
    birth_date = models.DateField(_('birth date'), blank=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        db_table = 'content\".\"person'

    def __str__(self):
        return self.full_name


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')


class Filmwork(TimeStampedMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True)
    certificate = models.TextField(_('certificate'), blank=True)
    file_path = models.FileField(_('file'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0)], blank=True)
    type = models.CharField(_('type'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='FilmworkGenre')
    persons = models.ManyToManyField(Person, through='FilmworkPerson')

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = "content\".\"film_work"


class FilmworkGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    filmwork = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'
        indexes = [
            models.Index(fields=['filmwork', 'genre']),
        ]


class FilmworkPerson(TimeStampedMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    filmwork = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=255)

    class Meta:
        db_table = 'content\".\"person_film_work'
        indexes = [
            models.Index(fields=['filmwork', 'person', 'role']),
        ]
