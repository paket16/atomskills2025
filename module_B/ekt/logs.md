*Сбор логов организуйте на машине YEKT-WORKER, на рабочем столе локального пользователя - yekt_admin с паролем P@ssw0rd. Директория $HOME/Desktop/Logs/, где NAME имя сервера, с которого был взят лог файл:*

*Логи собирать только веб-сервера на YEKT-BILLING и YEKT-DB;
Синхронизация логов происходит мгновенно;
Используйте любое техническое решение для реализации данной задачи.*

## Ответ AI

### **Настройка сбора логов на YEKT-WORKER**
Используем **rsyslog + inotify + rsync** для мгновенной синхронизации.

---

### **1. Настройка rsyslog на YEKT-BILLING и YEKT-DB**
Устанавливаем rsyslog и включаем передачу логов:
```bash
sudo apt update && sudo apt install rsyslog -y
```
Редактируем конфиг `/etc/rsyslog.conf`:
```bash
sudo nano /etc/rsyslog.conf
```
Добавляем в конец:
```
*.* @YEKT-WORKER:514
```
Перезапускаем rsyslog:
```bash
sudo systemctl restart rsyslog
```

---

### **2. Настройка приема логов на YEKT-WORKER**
Устанавливаем rsyslog и создаем директорию:
```bash
sudo apt install rsyslog -y
mkdir -p /home/yekt_admin/Desktop/Logs/
chown -R yekt_admin:yekt_admin /home/yekt_admin/Desktop/Logs/
```
Редактируем `/etc/rsyslog.conf`:
```bash
sudo nano /etc/rsyslog.conf
```
Добавляем:
```
$ModLoad imudp
$UDPServerRun 514

$template RemoteLogs,"/home/yekt_admin/Desktop/Logs/%HOSTNAME%.log"
*.* ?RemoteLogs
```
Перезапускаем rsyslog:
```bash
sudo systemctl restart rsyslog
```

---

### **3. Настройка мгновенной синхронизации логов**
Создаём скрипт на **YEKT-WORKER**:
```bash
sudo nano /home/yekt_admin/log_sync.sh
```
Добавляем:
```bash
#!/bin/bash
inotifywait -m /home/yekt_admin/Desktop/Logs/ -e create -e modify |
while read path action file; do
    rsync -avz /home/yekt_admin/Desktop/Logs/$file yekt_admin@YEKT-WORKER:/home/yekt_admin/Desktop/Logs/
done
```
Делаем исполняемым:
```bash
chmod +x /home/yekt_admin/log_sync.sh
```
Запускаем в фоне:
```bash
nohup /home/yekt_admin/log_sync.sh &
```

---

Теперь логи с **YEKT-BILLING** и **YEKT-DB** мгновенно синхронизируются на **YEKT-WORKER**! 🚀