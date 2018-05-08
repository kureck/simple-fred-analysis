--User: fred

create schema fred;

create table fred.gdpc1(
  id serial,
  observation_date date,
  value decimal,
  constraint pk_gdpc1_date_column primary key(observation_date)
);

create table fred.umcsent(
  id serial,
  observation_date date,
  value decimal,
  constraint pk_umcsent_date_column primary key(observation_date)
);

create table fred.unrate(
  id serial,
  observation_date date,
  value decimal,
  constraint pk_unrate_date_column primary key(observation_date)
);
