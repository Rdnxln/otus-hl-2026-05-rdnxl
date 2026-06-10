#!/bin/bash

# sn - is (s)ocial (n)etwork

# A. Demin

sudo apt install postgresql
#sudo apt install postgresql-15

# Создание БД, пользователей БД, таблиц и учетной записи пользователя

# пользователь-администратор, от имени которого мы выполняем DDL-запросы (определение объектов БД - таблицы, пользователи)
ADMUSER=db_admin
ADMPASS=123abc_

# пользователь-приложение, от имени которого мы выполняем DML-запросы (модификация данных - вставка, обновление, удаление)
APPUSER=app_user
APPPASS='321!123'


DBHOST=localhost
DBPORT=5432
DBNAME=sn


######## postgres/root stage

{
cat<<EOF
-- \set ON_ERROR_STOP off
-- Создаем администратора с паролем и правом создавать другие роли
CREATE USER $ADMUSER WITH PASSWORD '$ADMPASS' CREATEROLE;

-- Актуализируем пароль (если изменили при повторном запуске)
ALTER  USER $ADMUSER WITH PASSWORD '$ADMPASS';

-- Создаем базу данных и делаем пользователя db_admin её владельцем
CREATE DATABASE $DBNAME OWNER $ADMUSER;

EOF
} | sudo su postgres -c psql || { logger -s 'Возможно, нет прав суперпользователя'; exit 1;}

# временный файл для хранения параметров доступа к БД
touch       ~/.pgpass
chmod 0600  ~/.pgpass

######## administrator stage

DBUSER=$ADMUSER
DBPASS=$ADMPASS
# Формат: хост:порт:база_данных:пользователь:пароль
echo "$DBHOST:$DBPORT:$DBNAME:$DBUSER:$DBPASS" > ~/.pgpass

psql -h localhost  -U $DBUSER  -d sn <<EOF
  -- версия без первичных ключей
  -- (т.к. ключ - это индекс, а индексы использовать пока запрещено)

  -- таблица сеансов (сессий)
  DROP TABLE IF EXISTS sn_sess;
  CREATE TABLE IF NOT EXISTS sn_sess (
    sess_id    UUID         NOT NULL default gen_random_uuid(),
    user_id    UUID         NOT NULL,
    tact       TIMESTAMPTZ  NOT NULL default NOW()::TIMESTAMPTZ
  );

  -- таблица с пользователями
  DROP TABLE IF EXISTS sn_users;
  CREATE TABLE IF NOT EXISTS sn_users (
    -- требование уникальности, первичный ключ и 
    user_id     UUID         NOT NULL default gen_random_uuid(),
    login       VARCHAR(64)  NOT NULL,
    first_name  VARCHAR(64)  NOT NULL,
    second_name VARCHAR(64)  NOT NULL,
    birthdate   DATE         NOT NULL,
    biography   TEXT         NOT NULL,
    city_id     UUID         NOT NULL,
    sex         CHAR(1)              ,
    password    VARCHAR(32)  NOT NULL
  );

  -- таблица городов
  DROP TABLE IF EXISTS sn_cities;
  CREATE TABLE IF NOT EXISTS sn_cities (
    city_id     UUID         NOT NULL default gen_random_uuid(),
    city        VARCHAR(128) NOT NULL UNIQUE
             --                       ^ через UNIQUE мы неявно создали индекс,
             --                       хотя пользоваться индексами не рекомендуется
             -- Верхненовокутлумбетьево
             -- Старокозьмодемьяновское
             -- Александровск-Сахалинский
             -- Посёлок Центральной усадьбы совхоза имени 40-летия Великого Октября
  );

  -- создаем пользователя прикладного ПО, от которого будем выполнять действия с данными в БД
  DROP   USER $APPUSER;
  CREATE USER $APPUSER WITH PASSWORD '$APPPASS';
  ALTER  USER $APPUSER WITH PASSWORD '$APPPASS';
  GRANT SELECT, DELETE, UPDATE, INSERT ON sn_sess, sn_users, sn_cities TO $APPUSER;

EOF
rm    -f    ~/.pgpass

######## application stage

echo 'Если уже запущен uvicorn - перезапустите uvicorn, для переподключения к БД'
