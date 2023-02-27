# create a mysql that stores data in the container, not a volume (simpler, for dev env)
# create database for auth

# you might first create a project for mysql like this:
# ApiLogicServer create --project_name=my_project --db_url='mysql+pymysql://root:p@localhost:3306/my_project_db'
# cd my_project  # create your venv as usual...

# now, build MySQL image from this file
# cd devops/docker
# docker build -t my-org/my-project-mysql --file authdb_mysql.Dockerfile --rm .

# run container from built image
# docker run --name my-project-mysql-container --net dev-network -p 3306:3306 -d -e MYSQL_ROOT_PASSWORD=p my-org/my-project-mysql

# Now set up your mysql database.
# docker exec -it my-project-mysql-container /bin/bash
# bash> cd home
# bash> mkdir mysql_ddl

# on your local machine, copy the ddl (create tables) dump file
# cd devops/docker
# docker cp authdb_mysql.sql my-project-mysql-container:/home/mysql_ddl

# back to docker terminal...
# cd /var/lib/mysql
# mysql -p  # open mysql command line, then enter your super-secret password, `p`
# mysql> DROP DATABASE IF EXISTS `authdb`;
# mysql> CREATE DATABASE `authdb`;
# mysql> USE `authdb`;
# mysql> source /home/mysql_ddl/authdb_mysql.sql
# mysql> show databases;
# restore other database dumps as desired
# mysql> exit

# after adding users/roles (see below), you can dump authdb
# mysqldump -p authdb > /home/mysql_ddl/authdb_dump.sql
# bash> exit

# optionally add security
# create the Dockers' MySql authdb as above, using auth-db.sql
# cd my_project
# ApiLogicServer add-auth
# update config.py: SQLALCHEMY_DATABASE_URI_AUTHENTICATION = f'mysql+pymysql://root:p@localhost:3306/authdb'
# comment out sample lines in security/declare_security.py (lines around 27 or so)
# you should now be able to start server, login and access data
# add users via http://localhost:5656/admin/authentication_admin/

# Now convert container to image, and push to docker hub (change lines below to your account)
# docker commit my-project-mysql-container my-project-mysql-image
# docker tag my-project-mysql-image my-org/my-project-mysql-image:version1.0.0
# docker push my-org/my-project-mysql-image:version1.0.0

# thanks - https://medium.com/@stevenlandow/persist-share-dev-mysql-data-in-a-docker-image-with-commit-f9aa9910be0a

FROM mysql:8.0

RUN mkdir /var/lib/mysql-no-volume
CMD ["--datadir", "/var/lib/mysql-no-volume"]