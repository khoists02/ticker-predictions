CREATE TABLE sessions (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    ticker varchar NOT NULL,
    "date_time" varchar NOT NULL,
    "date" varchar NOT NULL,
    current_price float not null DEFAULT 0,
    previous_price float not null DEFAULT 0,
    CONSTRAINT sessions_pk PRIMARY KEY (id)
);