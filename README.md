### Инструкция по установке
##### Клонируем репозиторий на компьютер:

```bash
1) git@github.com:Fluttik/foodgram-project-react.git
2) cd foodgram-project-react
```

##### Cоздаем и активируем виртуальное окружение:
##### Windows

```bash
python -m venv venv 
```
```bash
source venv/Scripts/activate 
```

 ##### Linux
```bash
python3 -m venv venv 
```

```bash
source venv/bin/activate # Linux
```
##### Устанавливаем зависимости проекта:

```bash
cd backend
```
```
pip install -r requirements.txt
```

#####  Выполняем миграции:
```bash
python manage.py makemigrations
```
```
python manage.py migrate
```
##### поднимаем контейнеры для теста с фронтом
```bash
cd infra
```

```bash
docker-compose up --build
```