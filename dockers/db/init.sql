CREATE TYPE scrapper_data AS ENUM (
    'txt',
    'img'
);

CREATE TABLE orders (
    id         serial PRIMARY KEY,
    data_type  scrapper_data,
    url        text,
    status     text DEFAULT 'waiting',
    at         timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone 
);

CREATE TABLE traceback_log (
    order_id integer,
    tb       text
);
