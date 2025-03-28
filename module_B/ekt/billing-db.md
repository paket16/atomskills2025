*На сервере YEKT-BILLING развернута самописная система контроля за добычей горных пород, система работает с базой данных на сервере YEKT-DB, необходимо исправить следующие особенности платформы:*

*Сервер работает медленно, выявите причину и устраните неисправность;
Согласно внутреннему регламенту компании информация о добытых горных породах храниться только в течение последних 15 лет. Данные старше следует отправить на холодное хранение на сервер DC-STORAGE в каталог /crypto-folder, а из базы данных удалить.*

##Ответ AI:

### **Инструкция по устранению проблем**  

#### **1. Оптимизация работы сервера YEKT-BILLING**
1. **Проверка нагрузки системы:**  
   ```bash
   htop
   iostat -xm 5 3
   free -m
   ```
   - Если загружен CPU — определить процесс (`ps aux --sort=-%cpu | head -10`).
   - Если мало RAM, проверить swap (`free -m`).
   - Если диск загружен, проверить I/O (`iotop`).

2. **Проверка работы базы данных:**  
   - Посмотреть медленные запросы:  
     ```sql
     SELECT * FROM pg_stat_activity WHERE state = 'active';
     ```
   - Если нагрузка высокая, проверить индексы (`EXPLAIN ANALYZE` на медленных запросах).  
   - Очистить временные таблицы и логи, если они не нужны.  

3. **Оптимизация кода приложения** (если возможно):  
   - Проверить логи ошибок (`journalctl -u service-name --no-pager --since "10 minutes ago"`).  
   - Выяснить, есть ли блокировки в базе данных (`pg_locks` в PostgreSQL).  

---

#### **2. Архивация данных старше 15 лет**
1. **Создать SQL-запрос для выборки старых данных:**
   ```sql
   SELECT * FROM mining_data WHERE extraction_date < NOW() - INTERVAL '15 years';
   ```
   
2. **Экспортировать их в файл (например, CSV):**
   ```bash
   psql -U user -d database -c "COPY (SELECT * FROM mining_data WHERE extraction_date < NOW() - INTERVAL '15 years') TO STDOUT WITH CSV HEADER" > /tmp/archive.csv
   ```

3. **Перенести файл на DC-STORAGE:**
   ```bash
   scp /tmp/archive.csv user@dc-storage:/crypto-folder/
   ```

4. **Удалить устаревшие данные из базы:**
   ```sql
   DELETE FROM mining_data WHERE extraction_date < NOW() - INTERVAL '15 years';
   ```

5. **Автоматизировать процесс с помощью `cron`:**
   ```bash
   crontab -e
   ```
   Добавить строку:
   ```cron
   0 3 * * 1 /path/to/archive_script.sh
   ```