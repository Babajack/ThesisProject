DROP TABLE IF EXISTS tiere;

CREATE TABLE tiere
(
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT    NOT NULL,
    tierart TEXT    NOT NULL,
    preis   INTEGER NOT NULL
);

INSERT INTO tiere (name, tierart, preis)
VALUES ('Berta', 'Kuh', 1500),
       ('Emma', 'Huhn', 10),
       ('Tina', 'Huhn', 9),
       ('Babe', 'Schwein', 400),
       ('Wilbur', 'Schwein', 350),
       ('Ella', 'Schaf', 250),
       ('Anna', 'Huhn', 9),
       ('Heike', 'Schaf', 220),
       ('Anna', 'Kuh', 1450),
       ('Doris', 'Huhn', 11),
       ('Bianca', 'Kuh', 1700),
       ('Miss Piggy', 'Schwein', 500),
       ('Agata', 'Huhn', 15),
       ('Ferkel', 'Schwein', 300),
       ('Alice', 'Schaf', 200);

