CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE settings (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    ticker varchar NOT NULL,
    balance float not null DEFAULT 0,
    current float not null DEFAULT 0,
    CONSTRAINT settings_pk PRIMARY KEY (id)
);