##Projekt RPGSite

####Jakie biblioteki zostały użyte?

- _**django** (1.11b1)_
- _**mysqlclient** (1.3.10)_
- _**whitenoise** (3.3.0)_
- _**django-emoji** (2.2.0)_
- _**beautifulsoup4** (4.5.3)_
- _**lxml** (3.7.3)_

Aby zainstalować wszystkie biblioteki wystarczy użyć polecenia

```
pip install -r requirements.txt
```

####Preferowana wersja pythona?

```
Python 3.6.0 [32 bit]
```

####Jak stworzyć bazę danych MySQL?

```
DROP DATABASE IF EXISTS `rpgsite`;
CREATE DATABASE `rpgsite` DEFAULT CHAR SET utf8;
```

####Jak uruchomić serwer?

Dodanie pythona do PATH

```
set PYTHONPATH=<tutaj ścieżka do folderu pythona>
set PATH=%PYTHONPATH%\Scripts;%PYTHONPATH%;%PATH%
```

Uruchomienie serwera

```
python.exe manage.py makemigrations
python.exe manage.py migrate
python.exe manage.py collectstatic
python.exe manage.py runserver 0.0.0.0:80
```
