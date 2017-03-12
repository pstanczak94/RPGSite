@echo off

cmd /c %~dp0\usepython.bat %~dp0\print-version.py

echo.
echo  -^> makemigrations...
echo.

cmd /c %~dp0\usepython.bat %~dp0\manage.py makemigrations

echo.
echo  -^> migrate...
echo.

cmd /c %~dp0\usepython.bat %~dp0\manage.py migrate

echo.
echo  -^> collectstatic...

cmd /c %~dp0\usepython.bat %~dp0\manage.py collectstatic --noinput

echo.
echo  -^> runserver...
echo.

cmd /c %~dp0\usepython.bat %~dp0\manage.py runserver 0.0.0.0:80

echo.
