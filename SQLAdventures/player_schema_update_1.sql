DROP TABLE IF EXISTS tier;

CREATE TABLE tier
(
    nummer      INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    tierart     TEXT    NOT NULL,
    wert        INTEGER NOT NULL,
    besitzer_id INTEGER NOT NULL
);

INSERT INTO tier (name, tierart, wert, besitzer_id)
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
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    vorname    TEXT    NOT NULL,
    nachname   TEXT    NOT NULL,
    geschlecht TEXT    NOT NULL
);

INSERT INTO besitzer (vorname, nachname, geschlecht)
VALUES ('Hannes', 'Solo', 'männlich'),
       ('Jacky', 'Sparrow', 'weiblich'),
       ('Anna', 'Von Arrendelle', 'weiblich'),
       ('Froduard', 'Beutlin', 'männlich'),
       ('Jim', 'Knopfer', 'männlich'),
       ('Gandalfus', '', 'männlich'),
       ('Ariel', 'Stark', 'weiblich'),
       ('Sansaria', 'Stark', 'weiblich'),
       ('Ariel', '', 'weiblich'),
       ('Harald', 'Potter', 'männlich'),
       ('Rocky', 'Balbo', 'männlich');


DROP TABLE IF EXISTS ausruestung;

CREATE TABLE ausruestung
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    typ         TEXT    NOT NULL,
    name         TEXT    NOT NULL,
    besitzer_id INTEGER NOT NULL
);

INSERT INTO ausruestung (typ, name, besitzer_id)
VALUES ('Pistole', 'Jacky''s Pistole', 2),
       ('Piratenhut', 'Dreispitz', 2),
       ('Kettenhemd', 'Mithrilrüstung', 4),
       ('Schwert', 'Nadel', 7),
       ('Schwert', 'Stich', 4),
       ('Ring', 'Der eine Ring', 4),
       ('Zauberstab', 'Elderstab', 10),
       ('Boxhandschuhe', '', 11);
