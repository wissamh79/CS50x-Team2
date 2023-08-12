PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    phone TEXT,
    email TEXT NOT NULL UNIQUE,
    birthdate DATE,
    gender TEXT,
    patients_address TEXT,
    is_admin BOOLEAN NOT NULL DEFAULT False,
    is_doctor BOOLEAN NOT NULL DEFAULT False
);

CREATE TABLE IF NOT EXISTS Doctor (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT NOT NULL UNIQUE,
    age TEXT,
    gender TEXT,
    specialty TEXT,
    description TEXT,
    years_of_practice TEXT,
    doctors_address TEXT,
    is_available BOOLEAN NOT NULL DEFAULT False,
    user_id INTEGER UNIQUE,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS specialty (
    id INTEGER PRIMARY KEY,
    specialties TEXT NOT NULL,
    doctor_id INTEGER,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(id)
);

CREATE TABLE IF NOT EXISTS patient_reservation (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    doctor_id INTEGER,
    FOREIGN KEY (patient_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS patient_history (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    patient_reservation_id INTEGER,
    FOREIGN KEY (patient_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (patient_reservation_id) REFERENCES patient_reservation(id) ON DELETE CASCADE
);
