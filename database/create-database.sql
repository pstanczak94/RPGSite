-- 1. Drop database if exists

DROP DATABASE IF EXISTS `rpgsite`;

-- 2. Create database

CREATE DATABASE `rpgsite` DEFAULT CHARSET `utf8`;

-- 3. Import rpgsite-schema.sql

-- Make sure to uncheck this option:
-- [x] Enable foreign key checks
-- when importing schema

-- 4. Execute manage.py migrate

-- 5. You can run the server now