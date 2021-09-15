CREATE TABLE IF NOT EXISTS person(
    cpf TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    birth TEXT NOT NULL,
    PRIMARY KEY(cpf)
);

CREATE TABLE IF NOT EXISTS piece(
    id TEXT NOT NULL,
    value REAL NOT NULL,
    date TEXT NOT NULL,
    person_cpf TEXT,
    title TEXT,
    desc TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(person_cpf) REFERENCES person(cpf) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS exposition(
    id TEXT NOT NULL,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS creates(
    person_cpf TEXT NOT NULL,
    piece_id TEXT NOT NULL,
    FOREIGN KEY(person_cpf) REFERENCES person(cpf) ON DELETE CASCADE,
    FOREIGN KEY(piece_id) REFERENCES piece(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS visits(
    person_cpf TEXT NOT NULL,
    exposition_id TEXT NOT NULL,
    enter TEXT NOT NULL,
    leave TEXT NOT NULL,
    FOREIGN KEY(person_cpf) REFERENCES person(cpf) ON DELETE CASCADE,
    FOREIGN KEY(exposition_id) REFERENCES exposition(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS displays(
    piece_id TEXT NOT NULL,
    exposition_id TEXT NOT NULL,
    FOREIGN KEY(piece_id) REFERENCES piece(id) ON DELETE CASCADE,
    FOREIGN KEY(exposition_id) REFERENCES exposition(id) ON DELETE CASCADE
);
