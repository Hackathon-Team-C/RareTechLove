if [ "$MYSQL_DATABASE" ]; then
	echo "CREATE DATABASE IF NOT EXISTS \`$MYSQL_DATABASE\` ;" | "${mysql[@]}"
	mysql+=( "$MYSQL_DATABASE" )
fi

if [ "$MYSQL_USER" -a "$MYSQL_PASSWORD" ]; then
	echo "CREATE USER '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD' ;" | "${mysql[@]}"

	if [ "$MYSQL_DATABASE" ]; then
		echo "GRANT ALL ON \`$MYSQL_DATABASE\`.* TO '$MYSQL_USER'@'%' ;" | "${mysql[@]}"
	fi

	echo 'FLUSH PRIVILEGES ;' | "${mysql[@]}"
fi