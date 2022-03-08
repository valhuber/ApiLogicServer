#!/bin/bash

ApiLogicServer create --project_name=/localhost/classicmodels --db_url=mysql+pymysql://root:p@mysql-container:3306/classicmodels

ApiLogicServer create --project_name=/localhost/sakila --db_url=mysql+pymysql://root:p@mysql-container/sakila

ApiLogicServer create --project_name=/localhost/chinook --db_url=mysql+pymysql://root:p@mysql-container/Chinook

ApiLogicServer create --project_name=/localhost/postgres --db_url=postgresql://postgres:p@postgresql-container/postgres

ApiLogicServer create --project_name=/localhost/sqlserver --db_url='mssql+pyodbc://sa:posey386!@sqlsvr-container:1433/NORTHWND?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=no'

ApiLogicServer create --project_name=/localhost/ApiLogicServer --db_url=
