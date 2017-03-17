## Projekt RPGSite

#### O projekcie

Projekt RPGSite to stworzenie aplikacji webowej w popularnym frameworku 
webowym [Django](https://www.djangoproject.com) opierającym się na języku programowania 
Python. Zamysłem autora jest stworzenie unikalnego designu od podstaw dzięki 
znajomości takich języków jak HTML, CSS, JavaScript i oczywiście Python. 
Interfejs ma być przejrzysty, intuicyjny oraz funkcjonalny.

#### Zastosowanie

Projekt może być wykorzystany jako (często niezbędny) dodatek do serwera gry, 
który będzie stanowił bogaty interfejs. Założeniem autora jest osiągnięcie 
kompatybilności z przynajmniej jednym takim serwerem, którym najprawdopodobniej 
będzie [forgottenserver](https://github.com/otland/forgottenserver). 

#### Cel projektu

Zadaniem aplikacji webowej będzie stworzenie przyjaznego dla użytkownika 
środowiska, które będzie udostępniało następujące funkcjonalności:

- Tworzenie konta użytkownika (w tym sprawdzanie poprawności podanych danych: nazwa użytkownika, hasło i adres email)
- Weryfikacja adresu email użytkownika poprzez wysłanie na podany adres kodu weryfikacyjnego (lub gotowego linku do aktywacji)
- Możliwość zmiany hasła użytkownika
- Tworzenie postaci z możliwością wyboru określonych parametrów (tj. nazwa postaci, płeć, profesja, miasto, itp.), które będą miały odzwierciedlenie w świecie gry
- Przegląd postaci przypisanych do konta oraz możliwość ich usunięcia
- Możliwość utworzenia gildii, do której będą mogli wstąpić inni gracze, po spełnieniu odpowiednich warunków np. poziom postaci wyższy niż 50
- Możliwość zarządzania przez administratorów wszystkimi obiektami bazy danych gry w prosty, łatwy i przyjemny sposób
- Inne, na które autor jeszcze nie wpadł

#### Harmonogram pracy

- Tydzień 1 - stworzenie podstawowego szkieletu strony
- Tydzień 2 - dodanie możliwości tworzenia konta oraz autoryzowanego dostępu użytkowników
- Tydzień 3 - napisanie mechanizmu pozwalającego na tworzenie więcej niż jednej postaci przypisanej do konta
- Tydzień 4 - opracowanie systemu statystyk z możliwością grupowania i sortowania wszystkich postaci
- Tydzień 5 - dodanie możliwości tworzenia gildii z możliwością zapraszania do nich innych graczy
- Tydzień 6 - praca nad doskonaleniem interfejsu użytkownika, dodanie dynamicznych przejść między kolejnymi etapami tworzenia postaci
- Tydzień 7 - szukanie błędów w kodzie, poprawki błędów i ostateczne domknięcie projektu

#### Jakie biblioteki zostały użyte?

- _**django** (1.10.5)_
- _**pytz** (2016.10)_
- _**mysqlclient** (1.3.10)_
- _**whitenoise** (3.3.0)_
- _**django-emoji** (2.2.0)_
- _**beautifulsoup4** (4.5.3)_
- _**lxml** (3.7.3)_

Aby zainstalować wszystkie biblioteki wystarczy użyć polecenia

```
pip install -r requirements.txt
```

#### Preferowana wersja pythona?

```
Python 3.6.0 [32 bit]
```

#### Jak stworzyć bazę danych MySQL?

```
DROP DATABASE IF EXISTS `rpgsite`;
CREATE DATABASE `rpgsite` DEFAULT CHAR SET utf8;
```

#### Jak uruchomić serwer?

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

Aby poprawnie uruchomić serwer należy utworzyć folder `secret` w głównym folderze projektu.

Natomiast w folderze `secret` dwa kolejne foldery - `database` oraz `logs`.
