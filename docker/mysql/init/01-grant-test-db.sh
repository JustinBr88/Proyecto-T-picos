#!/bin/sh
# Se ejecuta una sola vez, al crear el contenedor por primera vez.
# Da permisos al usuario de la app sobre la base de tests (la de desarrollo ya
# la crea MySQL con MYSQL_DATABASE).
set -e
mysql -uroot -p"$MYSQL_ROOT_PASSWORD" <<SQL
GRANT ALL PRIVILEGES ON \`${TEST_DB_NAME}\`.* TO '${MYSQL_USER}'@'%';
FLUSH PRIVILEGES;
SQL
