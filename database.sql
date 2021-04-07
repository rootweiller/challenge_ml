-- public.config_extension definition

-- Drop table

-- DROP TABLE public.config_extension;

CREATE TABLE public.config_extension (
	id serial NOT NULL,
	"name" varchar(80) NULL,
	is_active bool NULL,
	created_at timestamptz(0) NULL
);


-- public.config_country definition

-- Drop table

-- DROP TABLE public.config_country;

CREATE TABLE public.config_country (
	id serial NOT NULL,
	site varchar(80) NULL,
	identification varchar(80) NULL,
	is_processed bool NULL
);


-- public.config_file definition

-- Drop table

-- DROP TABLE public.config_file;

CREATE TABLE public.config_file (
	id serial NOT NULL,
	"name" varchar(250) NULL,
	is_processed bool NULL,
	format varchar(80) NULL,
	separator varchar(80) NULL,
	created_at timestamptz(0) NULL
);


-- public.data_search_fact definition

-- Drop table

-- DROP TABLE public.data_search_fact;

CREATE TABLE public.data_search_fact (
	id serial NOT NULL,
	site varchar(80) NULL,
	identification varchar(80) NULL,
	category varchar(80) NULL,
	json_data jsonb NULL,
	created_at timestamptz(0) NULL,
	is_processed bool NULL
);


-- public.data_items definition

-- Drop table

-- DROP TABLE public.data_items;

CREATE TABLE public.data_items (
	id serial NOT NULL,
	price int8 NULL,
	start_time timestamptz(0) NULL,
	"name" varchar(250) NULL,
	description varchar(250) NULL,
	nickname varchar(250) NULL
);