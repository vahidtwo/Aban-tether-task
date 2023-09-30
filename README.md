# aban-tether

## project setup


1- SetUp venv
```
virtualenv venv
source venv/bin/activate
```

2- install Dependencies
```
pip install -r requirements.txt
```

3- spin off docker compose
```
docker-compose -f docker-compose.dev.yml up -d
```

4- create your env
```
cp .env.example .env
```

5- Create tables
```
python manage.py migrate
```

6- run the project
```
python manage.py runserver
```


