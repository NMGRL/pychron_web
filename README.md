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
   docker-compose exec web python manage.py migrate samples 0001 --fake
   docker-compose exec web python manage.py migrate
   ```
8. create a superuser
   ```shell
   docker-compose exec web python manage.py createsuperuser
   ```
9. Open a browser at `http://localhost:8000/samples/`

#MSSQL Support
To use a SQL Server database

1. set DATABASE_KIND=mssql in your .env.production file
2. use ```shell docker-compose build -f DockerfileMSSQL``` in step #5 instead