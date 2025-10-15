#!/bin/bash

# filepath: /home/lanntxyz/postgres/scripts/restore.sh

# Tên container Docker đang chạy PostgreSQL
CONTAINER_NAME="postgres-database-1"

# Thông tin cơ sở dữ liệu PostgreSQL
DB_NAME="xsmb_db_new"
DB_USER="uxsmb_new"
DB_PASSWORD="uKmZ79pA4gqy3L"

# File backup cần khôi phục
BACKUP_FILE="$1"

# Kiểm tra nếu file backup không được cung cấp
if [ -z "$BACKUP_FILE" ]; then
    echo "Vui lòng cung cấp đường dẫn đến file backup cần khôi phục."
    echo "Cách sử dụng: ./restore.sh /path/to/backup_file.sql"
    exit 1
fi

# Kiểm tra nếu file backup không tồn tại
if [ ! -f "$BACKUP_FILE" ]; then
    echo "File backup không tồn tại: $BACKUP_FILE"
    exit 1
fi

# Thực hiện khôi phục bằng docker exec
cat "$BACKUP_FILE" | docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME"

# Kiểm tra kết quả
if [ $? -eq 0 ]; then
    echo "Khôi phục thành công từ file: $BACKUP_FILE"
else
    echo "Khôi phục thất bại!"
    exit 1
fi