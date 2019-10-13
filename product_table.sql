CREATE TABLE product (
    id             integer NOT NULL PRIMARY KEY,
    name           varchar(50),
    stock          integer,
    price          decimal(18,2),
    description    varchar(255),
    category       varchar(50)
);
