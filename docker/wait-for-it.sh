#!/bin/bash
# wait-for-it.sh: Ждет доступности сервиса перед выполнением команды
# Источник: https://github.com/vishnubob/wait-for-it

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until nc -z "$host" "$port"; do
  >&2 echo "Ожидание доступности $host:$port..."
  sleep 1
done

>&2 echo "$host:$port доступен"
exec $cmd
