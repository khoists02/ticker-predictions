CREATE TABLE plays (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    ticker varchar NOT NULL,
    price float NOT NULL DEFAULT 0,
    in_price float NOT NULL DEFAULT 0,
    virtual boolean,
    played_at varchar null,
    CONSTRAINT plays_pk PRIMARY KEY (id)
);