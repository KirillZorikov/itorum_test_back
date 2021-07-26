# itorum_test_back

Django бэкенд для тествого задания компании Иторум.


### Ссылки проекта:

* Сайт: https://kz-projects.tk/itorum_test/
* Vue 3 фронтенд: https://github.com/KirillZorikov/itorum_test_front
* Api: https://kz-api.tk/itorum_test/api/v1/
* Admin panel: https://kz-api.tk/itorum_test/admin/
* Docker образ: [backend](https://hub.docker.com/repository/docker/kzorikov/itorum_test_back)


### Для запуска проекта локально необходимо:

- Скачать **env_itorum_test** и заполнить файлы с переменными окружения, удалив .template из имени.
- Скачать **docker-compose.yaml** и **nginx**.
- Запустить контейнеры:
```
docker-compose up -d
```
- Сделать миграции:
```
docker-compose exec itorum_test_prod python manage.py migrate
```
- Заполнить бд тестовыми данными:
```
docker-compose exec itorum_test_prod python manage.py fill_db_random
```
*Будут созданы суперпользователь, пользователь с правами на экспорт, 15 заказчиков и 500 заказов.*
- Собрать статику:
```
docker-compose exec itorum_test_prod python manage.py collectstatic
```


#### Также есть возможность запустить сайт на HTTPS.
#### Для этого, до запуска контейнеров, необходимо:
- Скачать **docker-compose.ssl.yaml** и **init-letsencrypt.sh**
- Заполнить [init-letsencrypt.sh](https://github.com/KirillZorikov/recipe_net/blob/master/init-letsencrypt.sh) и [app_ssl.conf](https://github.com/KirillZorikov/recipe_net/blob/master/nginx/app_ssl.conf)
данными для своего имени хоста.
- Сгенерировать HTTPS сертификаты:
```
chmod +x init-letsencrypt.sh
sudo ./init-letsencrypt.sh
```
- Заменить в инструкции все команды, с: 
```
docker-compose
```
на:
```
docker-compose -f docker-compose.ssl.yaml
```

