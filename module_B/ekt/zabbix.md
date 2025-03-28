*На сервере YEKT-DB уже есть сервер Zabbix:*

*Подключите к серверу HTTPS;
Настройте метрики Zabbix так, что в случае перегрузки CPU больше чем на 80% и переполнения диска более чем на 90%, Zabbix автоматически писал уведомления на почту - admin@company.cool.*

*Почтовый аккаунт admin@company.cool подключен к MSK-ADMINPC для доменного пользователя - admin_infra (импортируемый из CSV-файла)*

## Ответ AI
### **Настройка Zabbix с HTTPS и мониторингом перегрузок**  

---

## **1. Подключение HTTPS к Zabbix**  
### **1.1. Установим сертификаты (Let's Encrypt)**
```bash
sudo apt update
sudo apt install certbot python3-certbot-apache -y
```
Запрос сертификата:
```bash
sudo certbot --apache -d your-zabbix-domain.com
```
Обновление сертификата (добавим в cron):
```bash
echo "0 0 1 * * certbot renew --quiet" | sudo tee -a /etc/crontab
```

### **1.2. Настроим Apache для Zabbix**
Открываем конфиг:
```bash
sudo nano /etc/apache2/sites-available/zabbix.conf
```
Добавляем HTTPS:
```apache
<VirtualHost *:443>
    ServerName your-zabbix-domain.com
    DocumentRoot /usr/share/zabbix

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/your-zabbix-domain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/your-zabbix-domain.com/privkey.pem
</VirtualHost>
```
Перезапускаем:
```bash
sudo a2enmod ssl
sudo systemctl restart apache2
```
Теперь Zabbix доступен по HTTPS.

---

## **2. Настройка метрик для уведомлений**  
### **2.1. Создание триггеров в Zabbix**
#### **CPU > 80%**  
1. Перейти в Zabbix → Configuration → Hosts → Выбрать `YEKT-DB`.  
2. Вкладка **Triggers** → **Create Trigger**.  
3. Название: `High CPU Load`.  
4. Выражение:  
   ```
   {YEKT-DB:system.cpu.util[].avg(5m)}>80
   ```
5. Severity: **High**.  
6. Сохранить.

#### **Диск заполнен > 90%**  
1. Перейти в **Triggers** → **Create Trigger**.  
2. Название: `Disk Space Critical`.  
3. Выражение:  
   ```
   {YEKT-DB:vfs.fs.size[/,pused].last()} > 90
   ```
4. Severity: **High**.  
5. Сохранить.

---

## **3. Настройка уведомлений на почту**
### **3.1. Подключение почтового сервера**
1. В Zabbix: Administration → Media Types → **Email**.  
2. **SMTP server**: `smtp.company.cool`.  
3. **SMTP email**: `admin@company.cool`.  
4. **SMTP login**: `admin@company.cool`.  
5. **SMTP password**: `ваш_пароль` (лучше использовать API-токен).  
6. **SMTP port**: `587`.  
7. Нажать **Test**, сохранить.

### **3.2. Создание действия (Action)**
1. **Configuration** → **Actions** → **Create Action**.  
2. **Название:** `CPU or Disk Alert`.  
3. **Conditions:**  
   - **Trigger severity**: `High`.  
   - **Host**: `YEKT-DB`.  
4. **Operations → Add new operation:**  
   - Send message to **admin@company.cool**.  
5. **Сохранить.**

---

Теперь:  
✅ Zabbix работает по HTTPS.  
✅ Мониторит CPU и диск.  
✅ Автоматически шлёт письма на `admin@company.cool`. 