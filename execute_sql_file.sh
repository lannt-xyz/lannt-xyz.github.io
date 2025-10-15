#!/bin/bash

# filepath: /home/lanntxyz/postgres/scripts/reset_sequences.sh

# Tên container Docker đang chạy PostgreSQL
CONTAINER_NAME="postgres-database-1"

# Thông tin cơ sở dữ liệu PostgreSQL
DB_NAME="xsmb_db_new"
DB_USER="uxsmb_new"

# Lấy thư mục chứa script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Lấy tham số đầu tiên như path của sql file
if [ -z "$1" ]; then
    echo "Vui lòng cung cấp đường dẫn tới file SQL."
    exit 1
fi

SQL_FILE="$1"

# Kiểm tra file SQL có tồn tại không
if [ ! -f "$SQL_FILE" ]; then
    echo "File SQL không tồn tại: $SQL_FILE"
    exit 1
fi

# Copy file vào container
docker cp "$SQL_FILE" "$CONTAINER_NAME":/tmp/$(basename "$SQL_FILE")

# chạy file sql
docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -f /tmp/$(basename "$SQL_FILE")

# Kiểm tra kết quả
if [ $? -eq 0 ]; then
    echo "Thực thi file thành công: $SQL_FILE"
else
    echo "Thực thi file thất bại!"
    exit 1
fi