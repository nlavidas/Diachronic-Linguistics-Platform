--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13 (Debian 15.13-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: texts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.texts (
    id integer NOT NULL,
    filename text,
    language text,
    year integer,
    validated boolean DEFAULT false,
    quarantined boolean DEFAULT false
);


ALTER TABLE public.texts OWNER TO postgres;

--
-- Name: texts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.texts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.texts_id_seq OWNER TO postgres;

--
-- Name: texts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.texts_id_seq OWNED BY public.texts.id;


--
-- Name: valency_patterns; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.valency_patterns (
    id integer NOT NULL,
    text_id integer,
    verb text,
    pattern text,
    arguments text
);


ALTER TABLE public.valency_patterns OWNER TO postgres;

--
-- Name: valency_patterns_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.valency_patterns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.valency_patterns_id_seq OWNER TO postgres;

--
-- Name: valency_patterns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.valency_patterns_id_seq OWNED BY public.valency_patterns.id;


--
-- Name: texts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.texts ALTER COLUMN id SET DEFAULT nextval('public.texts_id_seq'::regclass);


--
-- Name: valency_patterns id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.valency_patterns ALTER COLUMN id SET DEFAULT nextval('public.valency_patterns_id_seq'::regclass);


--
-- Data for Name: texts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.texts (id, filename, language, year, validated, quarantined) FROM stdin;
\.


--
-- Data for Name: valency_patterns; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.valency_patterns (id, text_id, verb, pattern, arguments) FROM stdin;
\.


--
-- Name: texts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.texts_id_seq', 1, false);


--
-- Name: valency_patterns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.valency_patterns_id_seq', 1, false);


--
-- Name: texts texts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.texts
    ADD CONSTRAINT texts_pkey PRIMARY KEY (id);


--
-- Name: valency_patterns valency_patterns_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.valency_patterns
    ADD CONSTRAINT valency_patterns_pkey PRIMARY KEY (id);


--
-- Name: valency_patterns valency_patterns_text_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.valency_patterns
    ADD CONSTRAINT valency_patterns_text_id_fkey FOREIGN KEY (text_id) REFERENCES public.texts(id);


--
-- PostgreSQL database dump complete
--

