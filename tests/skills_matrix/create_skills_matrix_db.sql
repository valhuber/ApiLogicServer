
--
-- Name: certification; Type: TABLE; Schema: public; Owner: postgres
--

-- create database skills_matrix with owner postgres;
-- then, ApiLogicServer create --project_name=skills_matrix --db_url=postgresql://postgres:p@localhost/skills_matrix

CREATE TABLE public.certification (
    ident bigint NOT NULL,
    name character varying(128) NOT NULL,
    description_ident bigint NOT NULL,
    certification_authority_ident bigint
);


ALTER TABLE public.certification OWNER TO postgres;

--
-- Name: certification_authority; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.certification_authority (
    ident bigint NOT NULL,
    name character varying(128) NOT NULL,
    description_ident bigint NOT NULL
);


ALTER TABLE public.certification_authority OWNER TO postgres;

--
-- Name: certification_authority_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.certification_authority_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.certification_authority_ident_seq OWNER TO postgres;

--
-- Name: certification_authority_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.certification_authority_ident_seq OWNED BY public.certification_authority.ident;


--
-- Name: certification_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.certification_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.certification_ident_seq OWNER TO postgres;

--
-- Name: certification_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.certification_ident_seq OWNED BY public.certification.ident;


--
-- Name: description; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.description (
    ident bigint NOT NULL,
    description character varying(2000) NOT NULL
);


ALTER TABLE public.description OWNER TO postgres;

--
-- Name: description_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.description_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.description_ident_seq OWNER TO postgres;

--
-- Name: description_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.description_ident_seq OWNED BY public.description.ident;


--
-- Name: role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role (
    ident bigint NOT NULL,
    name character varying(128) NOT NULL,
    tenure_months integer DEFAULT 6,
    description_ident bigint NOT NULL,
    prerequisite_ident bigint,
    parent_ident bigint
);


ALTER TABLE public.role OWNER TO postgres;

--
-- Name: role_certification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_certification (
    ident bigint NOT NULL,
    role_ident bigint NOT NULL,
    certification_ident bigint NOT NULL
);


ALTER TABLE public.role_certification OWNER TO postgres;

--
-- Name: role_certification_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_certification_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.role_certification_ident_seq OWNER TO postgres;

--
-- Name: role_certification_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_certification_ident_seq OWNED BY public.role_certification.ident;


--
-- Name: role_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.role_ident_seq OWNER TO postgres;

--
-- Name: role_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_ident_seq OWNED BY public.role.ident;


--
-- Name: role_level; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_level (
    ident bigint NOT NULL,
    name character varying(128) NOT NULL
);


ALTER TABLE public.role_level OWNER TO postgres;

--
-- Name: role_level_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_level_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.role_level_ident_seq OWNER TO postgres;

--
-- Name: role_level_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_level_ident_seq OWNED BY public.role_level.ident;


--
-- Name: role_role_level; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_role_level (
    ident bigint NOT NULL,
    role_ident bigint NOT NULL,
    role_level_ident bigint NOT NULL,
    predecessor_ident bigint,
    successor_ident bigint
);


ALTER TABLE public.role_role_level OWNER TO postgres;

--
-- Name: role_role_level_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_role_level_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.role_role_level_ident_seq OWNER TO postgres;

--
-- Name: role_role_level_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_role_level_ident_seq OWNED BY public.role_role_level.ident;


--
-- Name: role_skill_skill_level; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_skill_skill_level (
    ident bigint NOT NULL,
    role_ident bigint NOT NULL,
    skill_skill_level_ident bigint NOT NULL
);


ALTER TABLE public.role_skill_skill_level OWNER TO postgres;

--
-- Name: role_skill_skill_level_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_skill_skill_level_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.role_skill_skill_level_ident_seq OWNER TO postgres;

--
-- Name: role_skill_skill_level_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_skill_skill_level_ident_seq OWNED BY public.role_skill_skill_level.ident;


--
-- Name: skill; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill (
    ident bigint NOT NULL,
    name character varying(128) NOT NULL,
    description_ident bigint NOT NULL,
    parent_ident bigint
);


ALTER TABLE public.skill OWNER TO postgres;

--
-- Name: skill_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill_category (
    ident bigint NOT NULL,
    name character varying(128) NOT NULL
);


ALTER TABLE public.skill_category OWNER TO postgres;

--
-- Name: skill_category_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skill_category_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.skill_category_ident_seq OWNER TO postgres;

--
-- Name: skill_category_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skill_category_ident_seq OWNED BY public.skill_category.ident;


--
-- Name: skill_category_skill; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill_category_skill (
    ident bigint NOT NULL,
    skill_category_ident bigint NOT NULL,
    skill_ident bigint NOT NULL
);


ALTER TABLE public.skill_category_skill OWNER TO postgres;

--
-- Name: skill_category_skill_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skill_category_skill_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.skill_category_skill_ident_seq OWNER TO postgres;

--
-- Name: skill_category_skill_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skill_category_skill_ident_seq OWNED BY public.skill_category_skill.ident;


--
-- Name: skill_certification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill_certification (
    ident bigint NOT NULL,
    skill_ident bigint NOT NULL,
    certification_ident bigint NOT NULL
);


ALTER TABLE public.skill_certification OWNER TO postgres;

--
-- Name: skill_certification_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skill_certification_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.skill_certification_ident_seq OWNER TO postgres;

--
-- Name: skill_certification_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skill_certification_ident_seq OWNED BY public.skill_certification.ident;


--
-- Name: skill_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skill_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.skill_ident_seq OWNER TO postgres;

--
-- Name: skill_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skill_ident_seq OWNED BY public.skill.ident;


--
-- Name: skill_level; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill_level (
    ident bigint NOT NULL,
    name character varying(128) NOT NULL,
    score smallint NOT NULL
);


ALTER TABLE public.skill_level OWNER TO postgres;

--
-- Name: skill_level_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skill_level_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.skill_level_ident_seq OWNER TO postgres;

--
-- Name: skill_level_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skill_level_ident_seq OWNED BY public.skill_level.ident;


--
-- Name: skill_skill_level; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skill_skill_level (
    ident bigint NOT NULL,
    skill_ident bigint NOT NULL,
    skill_level_ident bigint NOT NULL,
    description_ident bigint NOT NULL
);


ALTER TABLE public.skill_skill_level OWNER TO postgres;

--
-- Name: skill_skill_level_ident_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.skill_skill_level_ident_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.skill_skill_level_ident_seq OWNER TO postgres;

--
-- Name: skill_skill_level_ident_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.skill_skill_level_ident_seq OWNED BY public.skill_skill_level.ident;


--
-- Name: v_roles; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_roles AS
 SELECT r.name AS role_name,
    role_description.description AS role_description,
    s.name AS skill_name,
    skill_description.description AS skill_description,
    sl.name AS skill_level_name,
    sl.score AS skill_level_score,
    skill_level_description.description AS skill_level_description
   FROM (((((((((public.role r
     JOIN public.role_skill_skill_level rssl ON ((r.ident = rssl.role_ident)))
     JOIN public.skill_skill_level ssl ON ((rssl.skill_skill_level_ident = ssl.ident)))
     JOIN public.skill_level sl ON ((sl.ident = ssl.skill_level_ident)))
     JOIN public.skill s ON ((s.ident = ssl.skill_ident)))
     JOIN public.skill_category_skill scs ON ((s.ident = scs.skill_ident)))
     JOIN public.skill_category sc ON ((scs.skill_category_ident = sc.ident)))
     JOIN public.description skill_description ON ((s.description_ident = skill_description.ident)))
     JOIN public.description skill_level_description ON ((ssl.description_ident = skill_level_description.ident)))
     JOIN public.description role_description ON ((r.description_ident = role_description.ident)));


ALTER TABLE public.v_roles OWNER TO postgres;

--
-- Name: v_skills; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.v_skills AS
 SELECT s.name AS skill_name,
    skill_description.description AS skill_description,
    sc.name AS category_name,
    sl.name AS skill_level_name,
    sl.score,
    skill_level_description.description AS skill_level_description,
    parent_skill.name AS parent_skill
   FROM (((((((public.skill s
     JOIN public.skill_skill_level ssl ON ((s.ident = ssl.skill_ident)))
     JOIN public.skill_level sl ON ((ssl.skill_level_ident = sl.ident)))
     JOIN public.description skill_description ON ((s.description_ident = skill_description.ident)))
     JOIN public.description skill_level_description ON ((ssl.description_ident = skill_level_description.ident)))
     JOIN public.skill_category_skill scs ON ((s.ident = scs.skill_ident)))
     JOIN public.skill_category sc ON ((scs.skill_category_ident = sc.ident)))
     LEFT JOIN public.skill parent_skill ON ((parent_skill.ident = s.parent_ident)));


ALTER TABLE public.v_skills OWNER TO postgres;

--
-- Name: certification ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certification ALTER COLUMN ident SET DEFAULT nextval('public.certification_ident_seq'::regclass);


--
-- Name: certification_authority ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certification_authority ALTER COLUMN ident SET DEFAULT nextval('public.certification_authority_ident_seq'::regclass);


--
-- Name: description ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.description ALTER COLUMN ident SET DEFAULT nextval('public.description_ident_seq'::regclass);


--
-- Name: role ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role ALTER COLUMN ident SET DEFAULT nextval('public.role_ident_seq'::regclass);


--
-- Name: role_certification ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_certification ALTER COLUMN ident SET DEFAULT nextval('public.role_certification_ident_seq'::regclass);


--
-- Name: role_level ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_level ALTER COLUMN ident SET DEFAULT nextval('public.role_level_ident_seq'::regclass);


--
-- Name: role_role_level ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_role_level ALTER COLUMN ident SET DEFAULT nextval('public.role_role_level_ident_seq'::regclass);


--
-- Name: role_skill_skill_level ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_skill_skill_level ALTER COLUMN ident SET DEFAULT nextval('public.role_skill_skill_level_ident_seq'::regclass);


--
-- Name: skill ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill ALTER COLUMN ident SET DEFAULT nextval('public.skill_ident_seq'::regclass);


--
-- Name: skill_category ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_category ALTER COLUMN ident SET DEFAULT nextval('public.skill_category_ident_seq'::regclass);


--
-- Name: skill_category_skill ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_category_skill ALTER COLUMN ident SET DEFAULT nextval('public.skill_category_skill_ident_seq'::regclass);


--
-- Name: skill_certification ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_certification ALTER COLUMN ident SET DEFAULT nextval('public.skill_certification_ident_seq'::regclass);


--
-- Name: skill_level ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_level ALTER COLUMN ident SET DEFAULT nextval('public.skill_level_ident_seq'::regclass);


--
-- Name: skill_skill_level ident; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_skill_level ALTER COLUMN ident SET DEFAULT nextval('public.skill_skill_level_ident_seq'::regclass);


--
-- Data for Name: certification; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: certification_authority; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: description; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.description VALUES (40, 'database administrator');


--
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.role VALUES (40, 'dba', 6, 40, NULL, NULL);


--
-- Data for Name: role_certification; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: role_level; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.role_level VALUES (274, 'associate');
INSERT INTO public.role_level VALUES (275, 'senior');
INSERT INTO public.role_level VALUES (276, 'principal');
INSERT INTO public.role_level VALUES (277, 'manager');
INSERT INTO public.role_level VALUES (278, 'director');
INSERT INTO public.role_level VALUES (279, 'senior director');
INSERT INTO public.role_level VALUES (280, 'vice president');


--
-- Data for Name: role_role_level; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.role_role_level VALUES (193, 40, 274, NULL, 194);
INSERT INTO public.role_role_level VALUES (194, 40, 275, 193, 195);
INSERT INTO public.role_role_level VALUES (195, 40, 276, 194, 196);
INSERT INTO public.role_role_level VALUES (196, 40, 277, 195, 197);
INSERT INTO public.role_role_level VALUES (197, 40, 278, 196, 198);
INSERT INTO public.role_role_level VALUES (198, 40, 279, 197, 199);
INSERT INTO public.role_role_level VALUES (199, 40, 280, 198, NULL);


--
-- Data for Name: role_skill_skill_level; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: skill; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: skill_category; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: skill_category_skill; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: skill_certification; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: skill_level; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.skill_level VALUES (201, 'none', 0);
INSERT INTO public.skill_level VALUES (202, 'beginner', 1);
INSERT INTO public.skill_level VALUES (203, 'intermediate', 2);
INSERT INTO public.skill_level VALUES (204, 'advanced', 3);
INSERT INTO public.skill_level VALUES (205, 'expert', 4);


--
-- Data for Name: skill_skill_level; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Name: certification_authority_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.certification_authority_ident_seq', 1, false);


--
-- Name: certification_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.certification_ident_seq', 1, false);


--
-- Name: description_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.description_ident_seq', 40, true);


--
-- Name: role_certification_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.role_certification_ident_seq', 1, false);


--
-- Name: role_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.role_ident_seq', 40, true);


--
-- Name: role_level_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.role_level_ident_seq', 280, true);


--
-- Name: role_role_level_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.role_role_level_ident_seq', 199, true);


--
-- Name: role_skill_skill_level_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.role_skill_skill_level_ident_seq', 1, false);


--
-- Name: skill_category_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.skill_category_ident_seq', 1, false);


--
-- Name: skill_category_skill_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.skill_category_skill_ident_seq', 1, false);


--
-- Name: skill_certification_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.skill_certification_ident_seq', 1, false);


--
-- Name: skill_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.skill_ident_seq', 1, false);


--
-- Name: skill_level_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.skill_level_ident_seq', 205, true);


--
-- Name: skill_skill_level_ident_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.skill_skill_level_ident_seq', 1, false);


--
-- Name: certification_authority certification_authority_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certification_authority
    ADD CONSTRAINT certification_authority_name_key UNIQUE (name);


--
-- Name: certification_authority certification_authority_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certification_authority
    ADD CONSTRAINT certification_authority_pkey PRIMARY KEY (ident);


--
-- Name: certification certification_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certification
    ADD CONSTRAINT certification_name_key UNIQUE (name);


--
-- Name: certification certification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certification
    ADD CONSTRAINT certification_pkey PRIMARY KEY (ident);


--
-- Name: description description_description_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.description
    ADD CONSTRAINT description_description_key UNIQUE (description);


--
-- Name: description description_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.description
    ADD CONSTRAINT description_pkey PRIMARY KEY (ident);


--
-- Name: role_certification role_certification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_certification
    ADD CONSTRAINT role_certification_pkey PRIMARY KEY (ident);


--
-- Name: role_level role_level_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_level
    ADD CONSTRAINT role_level_name_key UNIQUE (name);


--
-- Name: role_level role_level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_level
    ADD CONSTRAINT role_level_pkey PRIMARY KEY (ident);


--
-- Name: role role_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_name_key UNIQUE (name);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (ident);


--
-- Name: role_role_level role_role_level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_role_level
    ADD CONSTRAINT role_role_level_pkey PRIMARY KEY (ident);


--
-- Name: role_skill_skill_level role_skill_skill_level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_skill_skill_level
    ADD CONSTRAINT role_skill_skill_level_pkey PRIMARY KEY (ident);


--
-- Name: skill_category skill_category_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_category
    ADD CONSTRAINT skill_category_name_key UNIQUE (name);


--
-- Name: skill_category skill_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_category
    ADD CONSTRAINT skill_category_pkey PRIMARY KEY (ident);


--
-- Name: skill_category_skill skill_category_skill_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_category_skill
    ADD CONSTRAINT skill_category_skill_pkey PRIMARY KEY (ident);


--
-- Name: skill_certification skill_certification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_certification
    ADD CONSTRAINT skill_certification_pkey PRIMARY KEY (ident);


--
-- Name: skill_level skill_level_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_level
    ADD CONSTRAINT skill_level_name_key UNIQUE (name);


--
-- Name: skill_level skill_level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_level
    ADD CONSTRAINT skill_level_pkey PRIMARY KEY (ident);


--
-- Name: skill skill_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill
    ADD CONSTRAINT skill_name_key UNIQUE (name);


--
-- Name: skill skill_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill
    ADD CONSTRAINT skill_pkey PRIMARY KEY (ident);


--
-- Name: skill_skill_level skill_skill_level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_skill_level
    ADD CONSTRAINT skill_skill_level_pkey PRIMARY KEY (ident);


--
-- Name: role_role_level unique_pairing; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_role_level
    ADD CONSTRAINT unique_pairing UNIQUE (role_ident, role_level_ident);


--
-- Name: skill_certification fk_certification; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_certification
    ADD CONSTRAINT fk_certification FOREIGN KEY (certification_ident) REFERENCES public.certification(ident);


--
-- Name: role_certification fk_certification; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_certification
    ADD CONSTRAINT fk_certification FOREIGN KEY (certification_ident) REFERENCES public.certification(ident);


--
-- Name: role fk_description; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT fk_description FOREIGN KEY (description_ident) REFERENCES public.description(ident);


--
-- Name: skill fk_description; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill
    ADD CONSTRAINT fk_description FOREIGN KEY (description_ident) REFERENCES public.description(ident);


--
-- Name: skill_skill_level fk_description; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_skill_level
    ADD CONSTRAINT fk_description FOREIGN KEY (description_ident) REFERENCES public.description(ident);


--
-- Name: certification_authority fk_description; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certification_authority
    ADD CONSTRAINT fk_description FOREIGN KEY (description_ident) REFERENCES public.description(ident);


--
-- Name: certification fk_description; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certification
    ADD CONSTRAINT fk_description FOREIGN KEY (description_ident) REFERENCES public.description(ident);


--
-- Name: role_role_level fk_role; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_role_level
    ADD CONSTRAINT fk_role FOREIGN KEY (role_ident) REFERENCES public.role(ident);


--
-- Name: role_skill_skill_level fk_role; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_skill_skill_level
    ADD CONSTRAINT fk_role FOREIGN KEY (role_ident) REFERENCES public.role(ident);


--
-- Name: role_certification fk_role; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_certification
    ADD CONSTRAINT fk_role FOREIGN KEY (role_ident) REFERENCES public.role(ident);


--
-- Name: role_role_level fk_role_level; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_role_level
    ADD CONSTRAINT fk_role_level FOREIGN KEY (role_level_ident) REFERENCES public.role_level(ident);


--
-- Name: skill_skill_level fk_skill; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_skill_level
    ADD CONSTRAINT fk_skill FOREIGN KEY (skill_ident) REFERENCES public.skill(ident);


--
-- Name: skill_category_skill fk_skill; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_category_skill
    ADD CONSTRAINT fk_skill FOREIGN KEY (skill_ident) REFERENCES public.skill(ident);


--
-- Name: skill_certification fk_skill; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_certification
    ADD CONSTRAINT fk_skill FOREIGN KEY (skill_ident) REFERENCES public.skill(ident);


--
-- Name: skill_category_skill fk_skill_category; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_category_skill
    ADD CONSTRAINT fk_skill_category FOREIGN KEY (skill_category_ident) REFERENCES public.skill_category(ident);


--
-- Name: skill_skill_level fk_skill_level; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill_skill_level
    ADD CONSTRAINT fk_skill_level FOREIGN KEY (skill_level_ident) REFERENCES public.skill_level(ident);


--
-- Name: role_skill_skill_level fk_skill_skill_level; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_skill_skill_level
    ADD CONSTRAINT fk_skill_skill_level FOREIGN KEY (skill_skill_level_ident) REFERENCES public.skill_skill_level(ident);


--
-- Name: certification opt_fk_certification_authority; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certification
    ADD CONSTRAINT opt_fk_certification_authority FOREIGN KEY (certification_authority_ident) REFERENCES public.certification_authority(ident);


--
-- Name: skill opt_fk_parent; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skill
    ADD CONSTRAINT opt_fk_parent FOREIGN KEY (parent_ident) REFERENCES public.skill(ident);


--
-- Name: role opt_fk_parent_ident; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT opt_fk_parent_ident FOREIGN KEY (parent_ident) REFERENCES public.role(ident);


--
-- Name: role_role_level opt_fk_predecessor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_role_level
    ADD CONSTRAINT opt_fk_predecessor FOREIGN KEY (predecessor_ident) REFERENCES public.role_role_level(ident);


--
-- Name: role opt_fk_prerequisite; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT opt_fk_prerequisite FOREIGN KEY (prerequisite_ident) REFERENCES public.role(ident);


--
-- Name: role_role_level opt_fk_successor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_role_level
    ADD CONSTRAINT opt_fk_successor FOREIGN KEY (successor_ident) REFERENCES public.role_role_level(ident);


--
-- PostgreSQL database dump complete
--
