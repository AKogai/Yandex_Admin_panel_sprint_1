from django.contrib import admin
from .models import Filmwork, Person, Genre, FilmworkPerson, FilmworkGenre


class PersonRoleInline(admin.TabularInline):
    model = FilmworkPerson
    extra = 0


class FilmworkGenreInline(admin.TabularInline):
    model = FilmworkGenre
    extra = 0


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating', 'created_at', 'updated_at')

    list_filter = ('type',)

    search_fields = ('title', 'description', 'id')

    fields = (
        'title', 'type', 'description', 'creation_date', 'certificate',
        'file_path', 'rating',
    )

    inlines = [
        PersonRoleInline,
        FilmworkGenreInline,
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')

    search_fields = ('name', 'description', 'id')

    fields = ('name', 'description')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'created_at', 'updated_at')

    search_fields = ('full_name', 'birth_date', 'id')

    fields = ('full_name', 'birth_date')
