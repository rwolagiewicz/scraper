FROM postgres:13

COPY dockers/db/init.sql init.sql
RUN cat init.sql  > /docker-entrypoint-initdb.d/init.sql
