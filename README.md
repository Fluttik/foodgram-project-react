
# Дипломный проект. Python backend разработчик.
#### «Фудграм» — сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
### Используемые технологии:
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
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


## Запуск на сервере
#### Копируем проект
```bash
git@github.com:Fluttik/foodgram-project-react.git
```

#### Заходим в папку infra
```bash
cd infra
```

#### Запускаем сборку докера
```bash
sudo docker compose -f docker-compose.production.yml up -d
```
#### Открываем контейнер backend
```bash
sudo docker exec -it infra_final-backend-1 bash
```
#### Запускаем миграции, создаем админа, и загружаем данные
```bash
python manage.py migrate
```
```bash
python manage.py createsuperuser
```
```bash
python manage.py load_csv
```
### Cервер запущен и работает.

### **Данные для входа в админку:**
```
Логин f@gmail.com
Пароль 1234
Адрес сервера fluttik.fun
```
Автор: Николай Королёв
