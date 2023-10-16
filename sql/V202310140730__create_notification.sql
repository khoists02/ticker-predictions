CREATE TABLE notifications (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    ticker varchar NOT NULL,
    per float NOT NULL DEFAULT 0,
    "close" float NOT NULL DEFAULT 0,
    "read" bool NOT NULL DEFAULT false,
    "updatedAt" varchar,
    CONSTRAINT notification_pk PRIMARY KEY (id)
);