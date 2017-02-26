
	Projekt RPGSite

1. Jakie biblioteki zostały użyte?

	- Django (1.11b1)
	- django-emoji (2.2.0)
	- whitenoise (3.3.0)
	- beautifulsoup4 (4.5.3)
	- lxml (3.7.3)
	- mysqlclient (1.3.10)
	- mod-wsgi (4.5.13)

2. Preferowana wersja pythona?

	Python 3.6.0 [32 bit]

2. Jak stworzyć bazę danych MySQL?

	DROP DATABASE IF EXISTS `rpgsite`;
	CREATE DATABASE `rpgsite` DEFAULT CHAR SET utf8;

3. Jak uruchomić serwer?

	Dodanie pythona do PATH:
	
	set PATH_TO_PYTHON=<tutaj ścieżka do folderu pythona>
	set PATH=%PATH_TO_PYTHON%\Scripts;%PATH_TO_PYTHON%;%PATH%
	
	Uruchomienie serwera:

	(python.exe/py.exe) manage.py makemigrations
	(python.exe/py.exe) manage.py migrate
	(python.exe/py.exe) manage.py collectstatic
	(python.exe/py.exe) manage.py runserver 0.0.0.0:80

4. Jak uruchomić wiersz poleceń MySQL?

	set PATH_TO_MYSQL=C:\Program Files\MySQL\MySQL Server 5.7\bin
	set PATH=%PATH_TO_MYSQL%;%PATH%
	(python.exe/py.exe) manage.py dbshell
