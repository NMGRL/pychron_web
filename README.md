# pychron_web
Django-based Web interface to a pychron db


#Quick Start
1. install docker
2. install docker-compose
3. clone repository
   ```shell
   git clone https://github.com/NMGRL/pychron_web
   cd pychron_web
   ```
4. edit `.env.production`
5. build the docker container
    ```shell
   docker-compose build
   ```
6. startup the server
   ```shell
   docker-compose up -d
   ```
7. migrate the database
   ```shell
   docker-compose exec web python manage.py migrate
   ```
8. create a superuser
   ```shell
   docker-compose exec web python manage.py createsuperuser
   ```
9. Open a browser at `http://localhost:8000/samples/`