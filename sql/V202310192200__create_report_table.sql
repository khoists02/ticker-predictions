CREATE TABLE report (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    ticker varchar NOT NULL,
    "date" varchar NOT NULL,
    increase float not null DEFAULT 0,
    decrease float not null DEFAULT 0,
    CONSTRAINT report_pk PRIMARY KEY (id),
    CONSTRAINT report_unique UNIQUE (ticker, date, increase, decrease)
);