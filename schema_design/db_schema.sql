-- Creating a separate schema for content:
CREATE SCHEMA IF NOT EXISTS content;

-- Genres of films:
CREATE TABLE IF NOT EXISTS content.genre(
    id          uuid PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    created_at  timestamp,
    updated_at  timestamp
);

-- Persons:
CREATE TABLE IF NOT EXISTS content.person(
    id          uuid PRIMARY KEY,
    full_name   TEXT NOT NULL,
    birth_date  DATE,
    created_at  timestamp,
    updated_at  timestamp
);

-- Films:
CREATE TABLE IF NOT EXISTS content.film_work(
    id              uuid PRIMARY KEY,
    title           TEXT NOT NULL,
    description     TEXT,
    creation_date   DATE,
    certificate     TEXT,
    file_path       TEXT,
    rating          FLOAT,
    type            TEXT NOT NULL,
    created_at      timestamp,
    updated_at      timestamp,
);

-- Relations film_genre:
CREATE TABLE IF NOT EXISTS content.genre_film_work(
    id              uuid PRIMARY KEY,
    film_work    uuid NOT NULL,
    genre        uuid NOT NULL,
    created_at      timestamp,
    FOREIGN KEY (film_work) REFERENCES content.film_work(id) ON DELETE CASCADE,
    FOREIGN KEY (genre) REFERENCES content.genre(id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX film_work_genre
    ON content.genre_film_work (film_work, genre);

-- Relations person_film
CREATE TABLE IF NOT EXISTS content.person_film_work(
    id              UUID PRIMARY KEY,
    film_work    uuid NOT NULL,
    person       uuid NOT NULL,
    role            TEXT NOT NULL,
    created_at      timestamp,

    FOREIGN KEY (film_work) REFERENCES content.film_work(id) ON DELETE CASCADE,
    FOREIGN KEY (person) REFERENCES content.person(id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX film_work_person_role
    ON content.person_film_work (film_work, person, role);
