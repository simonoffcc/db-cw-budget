PGDMP  :    '                |            home_budget    17.2    17.2 ,    L           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            M           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            N           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            O           1262    16449    home_budget    DATABASE        CREATE DATABASE home_budget WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE home_budget;
                     postgres    false            �            1255    16507    check_closed_period()    FUNCTION     �  CREATE FUNCTION public.check_closed_period() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    period_exists BOOLEAN;
BEGIN
    SELECT EXISTS(
        SELECT 1
        FROM balances
        WHERE NEW.operation_date BETWEEN balance_date AND (balance_date + INTERVAL '1 month' - INTERVAL '1 day')
    ) INTO period_exists;

    IF period_exists THEN
        RAISE EXCEPTION 'Cannot insert operation in a closed period.';
    END IF;

    RETURN NEW;
END;
$$;
 ,   DROP FUNCTION public.check_closed_period();
       public               postgres    false            �            1255    16505    check_non_zero_amounts()    FUNCTION     	  CREATE FUNCTION public.check_non_zero_amounts() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.income_amount = 0 AND NEW.expense_amount = 0 THEN
        RAISE EXCEPTION 'Operation amounts cannot both be zero.';
    END IF;
    RETURN NEW;
END;
$$;
 /   DROP FUNCTION public.check_non_zero_amounts();
       public               postgres    false            �            1255    16510    disable_trigger(text, text)    FUNCTION     �   CREATE FUNCTION public.disable_trigger(table_name text, trigger_name text) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    EXECUTE format('ALTER TABLE %I DISABLE TRIGGER %I', table_name, trigger_name);
END;
$$;
 J   DROP FUNCTION public.disable_trigger(table_name text, trigger_name text);
       public               postgres    false            �            1255    16511    enable_trigger(text, text)    FUNCTION     �   CREATE FUNCTION public.enable_trigger(table_name text, trigger_name text) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    EXECUTE format('ALTER TABLE %I ENABLE TRIGGER %I', table_name, trigger_name);
END;
$$;
 I   DROP FUNCTION public.enable_trigger(table_name text, trigger_name text);
       public               postgres    false            �            1255    16501    generate_balances()    FUNCTION     e  CREATE FUNCTION public.generate_balances() RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    current_balance_id INT;
    start_date DATE;
    end_date DATE;
    income_sum INT;
    expense_sum INT;
    net_profit INT;
BEGIN
    FOR start_date IN SELECT DISTINCT date_trunc('month', operation_date) FROM operations WHERE balance_id IS NULL LOOP
        end_date := start_date + INTERVAL '1 month' - INTERVAL '1 day';

        SELECT COALESCE(SUM(income_amount), 0) INTO income_sum FROM operations WHERE operation_date BETWEEN start_date AND end_date AND balance_id IS NULL;
        SELECT COALESCE(SUM(expense_amount), 0) INTO expense_sum FROM operations WHERE operation_date BETWEEN start_date AND end_date AND balance_id IS NULL;
        net_profit := income_sum - expense_sum;

        INSERT INTO balances (income_sum, expense_sum, net_profit, balance_date) VALUES (income_sum, expense_sum, net_profit, start_date) RETURNING id INTO current_balance_id;

        UPDATE operations SET balance_id = current_balance_id WHERE operation_date BETWEEN start_date AND end_date AND balance_id IS NULL;
    END LOOP;
END;
$$;
 *   DROP FUNCTION public.generate_balances();
       public               postgres    false            �            1255    16513 $   generate_balances_without_triggers()    FUNCTION     6  CREATE FUNCTION public.generate_balances_without_triggers() RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Отключить триггеры
    PERFORM disable_trigger('operations', 'non_zero_amounts_trigger');
    PERFORM disable_trigger('operations', 'closed_period_trigger');

    -- Создаём балансы
    PERFORM generate_balances();

    -- Включить триггеры обратно
    PERFORM enable_trigger('operations', 'non_zero_amounts_trigger');
    PERFORM enable_trigger('operations', 'closed_period_trigger');
END;
$$;
 ;   DROP FUNCTION public.generate_balances_without_triggers();
       public               postgres    false            �            1255    16512    unbalance_operations()    FUNCTION       CREATE FUNCTION public.unbalance_operations() RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Отключить триггеры
    PERFORM disable_trigger('operations', 'non_zero_amounts_trigger');
    PERFORM disable_trigger('operations', 'closed_period_trigger');

    -- Обновить операции, сбросив balance_id для операций, принадлежащих данному балансу
    UPDATE operations
    SET balance_id = NULL
    WHERE balance_id IS NOT NULL;

    -- Удалить баланс
    DELETE FROM balances;

    -- Включить триггеры обратно
    PERFORM enable_trigger('operations', 'non_zero_amounts_trigger');
    PERFORM enable_trigger('operations', 'closed_period_trigger');
END;
$$;
 -   DROP FUNCTION public.unbalance_operations();
       public               postgres    false            �            1259    16454    articles    TABLE     d   CREATE TABLE public.articles (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);
    DROP TABLE public.articles;
       public         heap r       postgres    false            �            1259    16457    articles_id_seq    SEQUENCE     �   CREATE SEQUENCE public.articles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.articles_id_seq;
       public               postgres    false    217            P           0    0    articles_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.articles_id_seq OWNED BY public.articles.id;
          public               postgres    false    218            �            1259    16458    balances    TABLE     �   CREATE TABLE public.balances (
    id integer NOT NULL,
    expense_sum integer NOT NULL,
    income_sum integer NOT NULL,
    net_profit integer NOT NULL,
    balance_date date NOT NULL
);
    DROP TABLE public.balances;
       public         heap r       postgres    false            �            1259    16461    balances_id_seq    SEQUENCE     �   CREATE SEQUENCE public.balances_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.balances_id_seq;
       public               postgres    false    219            Q           0    0    balances_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.balances_id_seq OWNED BY public.balances.id;
          public               postgres    false    220            �            1259    16462 
   operations    TABLE     �   CREATE TABLE public.operations (
    id integer NOT NULL,
    article_id integer NOT NULL,
    expense_amount integer DEFAULT 0,
    income_amount integer DEFAULT 0,
    operation_date date NOT NULL,
    balance_id integer
);
    DROP TABLE public.operations;
       public         heap r       postgres    false            �            1259    16467    operations_id_seq    SEQUENCE     �   CREATE SEQUENCE public.operations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.operations_id_seq;
       public               postgres    false    221            R           0    0    operations_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.operations_id_seq OWNED BY public.operations.id;
          public               postgres    false    222            �            1259    16468    users    TABLE     C  CREATE TABLE public.users (
    id integer NOT NULL,
    login character varying(50) NOT NULL,
    password_hash character varying(256) NOT NULL,
    role character varying(10),
    CONSTRAINT users_role_check CHECK (((role)::text = ANY (ARRAY[('admin'::character varying)::text, ('reader'::character varying)::text])))
);
    DROP TABLE public.users;
       public         heap r       postgres    false            �            1259    16472    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public               postgres    false    223            S           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public               postgres    false    224            �           2604    16473    articles id    DEFAULT     j   ALTER TABLE ONLY public.articles ALTER COLUMN id SET DEFAULT nextval('public.articles_id_seq'::regclass);
 :   ALTER TABLE public.articles ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    218    217            �           2604    16474    balances id    DEFAULT     j   ALTER TABLE ONLY public.balances ALTER COLUMN id SET DEFAULT nextval('public.balances_id_seq'::regclass);
 :   ALTER TABLE public.balances ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    220    219            �           2604    16475    operations id    DEFAULT     n   ALTER TABLE ONLY public.operations ALTER COLUMN id SET DEFAULT nextval('public.operations_id_seq'::regclass);
 <   ALTER TABLE public.operations ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    222    221            �           2604    16476    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    224    223            B          0    16454    articles 
   TABLE DATA           ,   COPY public.articles (id, name) FROM stdin;
    public               postgres    false    217   �=       D          0    16458    balances 
   TABLE DATA           Y   COPY public.balances (id, expense_sum, income_sum, net_profit, balance_date) FROM stdin;
    public               postgres    false    219   7>       F          0    16462 
   operations 
   TABLE DATA           o   COPY public.operations (id, article_id, expense_amount, income_amount, operation_date, balance_id) FROM stdin;
    public               postgres    false    221   �>       H          0    16468    users 
   TABLE DATA           ?   COPY public.users (id, login, password_hash, role) FROM stdin;
    public               postgres    false    223   �@       T           0    0    articles_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.articles_id_seq', 16, true);
          public               postgres    false    218            U           0    0    balances_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.balances_id_seq', 105, true);
          public               postgres    false    220            V           0    0    operations_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.operations_id_seq', 58, true);
          public               postgres    false    222            W           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 2, true);
          public               postgres    false    224            �           2606    16478    articles articles_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.articles
    ADD CONSTRAINT articles_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.articles DROP CONSTRAINT articles_pkey;
       public                 postgres    false    217            �           2606    16480    balances balances_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.balances
    ADD CONSTRAINT balances_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.balances DROP CONSTRAINT balances_pkey;
       public                 postgres    false    219            �           2606    16482    operations operations_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.operations
    ADD CONSTRAINT operations_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.operations DROP CONSTRAINT operations_pkey;
       public                 postgres    false    221            �           2606    16484    users users_login_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_login_key UNIQUE (login);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_login_key;
       public                 postgres    false    223            �           2606    16486    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    223            �           2620    16508     operations closed_period_trigger    TRIGGER     �   CREATE TRIGGER closed_period_trigger BEFORE INSERT OR UPDATE ON public.operations FOR EACH ROW EXECUTE FUNCTION public.check_closed_period();
 9   DROP TRIGGER closed_period_trigger ON public.operations;
       public               postgres    false    229    221            �           2620    16506 #   operations non_zero_amounts_trigger    TRIGGER     �   CREATE TRIGGER non_zero_amounts_trigger BEFORE INSERT OR UPDATE ON public.operations FOR EACH ROW EXECUTE FUNCTION public.check_non_zero_amounts();
 <   DROP TRIGGER non_zero_amounts_trigger ON public.operations;
       public               postgres    false    225    221            �           2606    16490 %   operations operations_article_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.operations
    ADD CONSTRAINT operations_article_id_fkey FOREIGN KEY (article_id) REFERENCES public.articles(id);
 O   ALTER TABLE ONLY public.operations DROP CONSTRAINT operations_article_id_fkey;
       public               postgres    false    217    4772    221            �           2606    16495 %   operations operations_balance_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.operations
    ADD CONSTRAINT operations_balance_id_fkey FOREIGN KEY (balance_id) REFERENCES public.balances(id);
 O   ALTER TABLE ONLY public.operations DROP CONSTRAINT operations_balance_id_fkey;
       public               postgres    false    221    219    4774            B   z   x����@D��b��`(�b�Gr� �!��������ێ�G83o�Rh��+AWdg��5Zw����:��Hҍp��RxZ����[�Q�LLLvr<����.�oz/�]������.R�      D   �   x�=��C!���^�<^0����Y~����pc@����ޤ7�3�PXڐ<F�֡a�}\�ܚ�Sѵ���46��Xi��Y1�}�S�U�t�k��9$�2�:�u�f~Վ*�>гޗyo?h�P�9��k�At�2^�W��Zַ�;���y���9:      F   �  x�]�ˑ$1Dϒ/��W�/�hZ��k��T2d�����|O���U�������h�QN����tJ"�^�o�"�<�=`�d��*b*��jB�"�{H6�
�C��H"'�h˶^I<Tm�$�x���Uf�U8[[�n $��PO+� �B<�`.����B��t��9tb&5"An+���7h���K���՚H{-��u�5s�R���A-_a]
�
�)n�
Y���n#��ǰɻ��P��T��~@�kuH�{D�u^�|�����1��9��U���!~��P������-v��^��6t�1��:+��`����gS�ۀ�����~�oV\!�ʝ�+�Sl�����K�ؿ5"=���D�[��}oRo$z�����f���e�&h�/%��m��P���$�Mt'`tH�\���9��~ʈ      H   �   x��;�  �Sa�ߥ�1�)I�v���7=(��z݅Tl� ��&�&�.LX���6�5ܒL�?O�b�:�����J�,؁s�CE'�Ƣ4��k̹IF��->��;lǻ>���I,k     