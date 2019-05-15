In outer mbsserver where the file manage.py is:
python3 -m django --version				- django version
django-admin startproject project_name			- create new project
python3 manage.py runserver				- to run the server on port 8000
python3 manage.py runserver port_number			- to run on a specific port
python3 manage.py startapp app_name			- to create an app
python3 manage.py makemigrations mbsapi 		- to sync models with database


In app_name/migrations you can see migration files:
python3 manage.py sqlmigrate app_name migration_number

python3 manage.py sqlflush				- drop tables
python3 manage.py shell					- starts an shell to test your models
							- you should first import your models
