DROP TABLE IF EXISTS tiere;

CREATE TABLE tiere
(
    nummer  INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT    NOT NULL,
    tierart TEXT    NOT NULL,
    wert   INTEGER NOT NULL,
    besitzer_id INTEGER NOT NULL
);

INSERT INTO tiere (name, tierart, wert, besitzer_id)
VALUES ('Berta', 'Kuh', 1500, 1),
       ('Emma', 'Huhn', 10, 2),
       ('Tina', 'Huhn', 9, 1),
       ('Babe', 'Schwein', 400, 3),
       ('Wilbur', 'Schwein', 350, 4),
       ('Ella', 'Schaf', 250, 2),
       ('Anna', 'Huhn', 9, 2),
       ('Heike', 'Schaf', 220, 3),
       ('Anna', 'Kuh', 1450, 5),
       ('Doris', 'Huhn', 11, 6),
       ('Bianca', 'Kuh', 900, 5),
       ('Miss Piggy', 'Schwein', 500, 6),
       ('Agata', 'Huhn', 15, 10),
       ('Ferkel', 'Schwein', 300, 4),
       ('Anna', 'Schwein', 250, 8),
       ('Doris', 'Schwein', 400, 8),
       ('Alice', 'Schaf', 200, 1);


DROP TABLE IF EXISTS besitzer;

CREATE TABLE besitzer
(
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    vorname    TEXT    NOT NULL,
    nachname TEXT    NOT NULL,
    "alter"   INTEGER NOT NULL,
    geschlecht TEXT NOT NULL
);

INSERT INTO besitzer (vorname, nachname, "alter", geschlecht)
VALUES ('Hannes', 'Solo', 25, 'männlich'),
       ('Jacky', 'Sparrow', 38, 'weiblich'),
       ('Anna', 'Von Arrendelle', 38, 'weiblich'),
       ('Froduard', 'Beutlin', 18, 'männlich'),
       ('Jim', 'Knopfer', 21, 'männlich'),
       ('Gandalfus', '', 71, 'männlich'),
       ('Ariel', 'Stark', 18, 'weiblich'),
       ('Sansaria', 'Stark', 26, 'weiblich'),
       ('Ariel', '', 28, 'weiblich'),
       ('Harald', 'Potter', 36, 'männlich'),
       ('Rocky', 'Balbo', 49, 'männlich');