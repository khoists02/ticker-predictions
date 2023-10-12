CREATE TABLE favorites (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    ticker varchar NOT NULL,
    symbol varchar NOT NULL,
    CONSTRAINT favorites_pk PRIMARY KEY (id)
);