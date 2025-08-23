#!/bin/bash

BACKUP_DIR="./backups"

echo "🛠️ Менеджер бэкапов Metabase"
echo "=============================="
echo ""

while true; do
    echo "1. Создать бэкап"
    echo "2. Восстановить из бэкапа"
    echo "3. Показать список бэкапов"
    echo "4. Удалить старые бэкапы"
    echo "5. Выйти"
    echo ""
    read -p "🔢 Выберите действие (1-5): " action

    case $action in
        1)
            echo "📦 Создание бэкапа..."
            ./backup_scripts/backup_metabase.sh
            ;;
        2)
            echo "🔄 Восстановление из бэкапа..."
            ./backup_scripts//restore_metabase.sh
            ;;
        3)
            echo "📋 Список бэкапов:"
            if [ -d "$BACKUP_DIR" ]; then
                ls -la "$BACKUP_DIR"/*.mv.db 2>/dev/null | awk '{print $9 " (" $5 " bytes, " $6 " " $7 " " $8 ")"}'
            else
                echo "❌ Директория с бэкапами не существует"
            fi
            ;;
        4)
            echo "🗑️ Удаление старых бэкапов..."
            read -p "❓ Сколько последних бэкапов оставить? (например, 10): " keep
            if [[ "$keep" =~ ^[0-9]+$ ]]; then
                ls -t "$BACKUP_DIR"/*.mv.db 2>/dev/null | tail -n +$(($keep+1)) | xargs rm -f
                echo "✅ Удалены старые бэкапы, оставлено $keep последних"
            else
                echo "❌ Неверное число"
            fi
            ;;
        5)
            echo "👋 Выход"
            exit 0
            ;;
        *)
            echo "❌ Неверный выбор"
            ;;
    esac

    echo ""
    echo "-----------------------------"
    echo ""
done