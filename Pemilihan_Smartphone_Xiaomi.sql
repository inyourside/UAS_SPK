PGDMP     9    1                {            Pemilihan_Smartphone_Xiaomi    14.9    14.9     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16395    Pemilihan_Smartphone_Xiaomi    DATABASE     �   CREATE DATABASE "Pemilihan_Smartphone_Xiaomi" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';
 -   DROP DATABASE "Pemilihan_Smartphone_Xiaomi";
                postgres    false            �            1259    16436 
   tbl_xiaomi    TABLE     R  CREATE TABLE public.tbl_xiaomi (
    no integer NOT NULL,
    type character varying(255),
    kamera character varying(255),
    baterai character varying(255),
    layar character varying(255),
    ram character varying(255),
    processor character varying(255),
    harga character varying(255),
    benefit character varying(255)
);
    DROP TABLE public.tbl_xiaomi;
       public         heap    postgres    false            �            1259    16435    tbl_xiaomi_nomor_seq    SEQUENCE     �   CREATE SEQUENCE public.tbl_xiaomi_nomor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.tbl_xiaomi_nomor_seq;
       public          postgres    false    210            �           0    0    tbl_xiaomi_nomor_seq    SEQUENCE OWNED BY     J   ALTER SEQUENCE public.tbl_xiaomi_nomor_seq OWNED BY public.tbl_xiaomi.no;
          public          postgres    false    209            \           2604    16439    tbl_xiaomi no    DEFAULT     q   ALTER TABLE ONLY public.tbl_xiaomi ALTER COLUMN no SET DEFAULT nextval('public.tbl_xiaomi_nomor_seq'::regclass);
 <   ALTER TABLE public.tbl_xiaomi ALTER COLUMN no DROP DEFAULT;
       public          postgres    false    210    209    210            �          0    16436 
   tbl_xiaomi 
   TABLE DATA           f   COPY public.tbl_xiaomi (no, type, kamera, baterai, layar, ram, processor, harga, benefit) FROM stdin;
    public          postgres    false    210          �           0    0    tbl_xiaomi_nomor_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.tbl_xiaomi_nomor_seq', 10, true);
          public          postgres    false    209            ^           2606    16443    tbl_xiaomi tbl_xiaomi_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.tbl_xiaomi
    ADD CONSTRAINT tbl_xiaomi_pkey PRIMARY KEY (no);
 D   ALTER TABLE ONLY public.tbl_xiaomi DROP CONSTRAINT tbl_xiaomi_pkey;
       public            postgres    false    210            �   �  x������0�y�9�*B�`�m��JM�U�J{��$��
dH���װKB�E	$υ��3Â<H̕�#����<�X����tH+�M����MB'X�̶nVߖo�e>�%!ܽ'�3,b��<s0�.\ω�ȡ��/��F���P�P�+�
a/�-f;bQ�̠���,�=�g��9��9U"E�W�)���p��Z/j{፩]�:�!wٕ���	�O�X�þ��8��m0����=C���_*�NrƧ���0+�w�ޭ��\���W�|��ؤ�?�\H���Cٳ5t�{��E'���!�V6�'����Gd��a$��4����c����q,�P򠬰e��%x$��~g���qa�᜕ufo)+���ig�s7�A�^��h�\��<���9�
+��������D,��íT"+eu4q纸|oЌJ�0�RTh��0����U�;�ص�����X��I��     