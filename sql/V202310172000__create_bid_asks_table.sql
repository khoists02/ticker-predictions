CREATE TABLE bid_asks (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    ticker varchar NOT NULL,
    "updated_at" varchar NOT NULL,
    ask float not null DEFAULT 0,
    bid float not null DEFAULT 0,
    ask_size float not null DEFAULT 0,
    bid_size float not null DEFAULT 0,
    CONSTRAINT bid_asks_pk PRIMARY KEY (id)
);