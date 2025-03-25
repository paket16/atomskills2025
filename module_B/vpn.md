Вот готовые скрипты для настройки отказоустойчивых GRE-туннелей между роутерами по топологии:
![topology](../assets/VPN_Topology.png)

### 1. Основные скрипты настройки туннелей

#### Для DC-RTR-1 (`/usr/local/bin/setup_tunnels_dc1.sh`):
```bash
#!/bin/bash

# ===== CONFIGURATION =====
# Основной туннель в Москву
MSK_REMOTE="188.121.90.2"   # MSK-RTR внешний IP
MSK_LOCAL="200.100.100.20"     # DC-RTR-1 внешний IP
MSK_TUN_IP="10.7.7.1/30"

# Резервный туннель в Екатеринбург (через DC-RTR-2)
EKT_REMOTE="10.15.10.2"    # DC-RTR-2 внутренний IP
EKT_LOCAL="10.15.10.3"     # DC-RTR-1 внутренний IP
EKT_TUN_IP="10.8.8.1/30"

MAIL_SERVER="10.15.10.100" # IP почтового сервера
# ========================

# Настройка основного туннеля в Москву
ip tunnel add gre-msk mode gre remote $MSK_REMOTE local $MSK_LOCAL ttl 255
ip link set gre-msk up
ip addr add $MSK_TUN_IP dev gre-msk

# Настройка резервного туннеля в Екатеринбург
# Я не уверен в корректной работе этого блока
ip tunnel add gre-ekt mode gre remote $EKT_REMOTE local $EKT_LOCAL ttl 255
ip link set gre-ekt up
ip addr add $EKT_TUN_IP dev gre-ekt

# Включение маршрутизации. Стоит заменить на: echo net.ipv4.ip_forward=1 > /etc/sysctl.conf
#sysctl -p
#echo 1 > /proc/sys/net/ipv4/ip_forward

# Настройка маршрутов по умолчанию
ip route replace $MAIL_SERVER via ${MSK_TUN_IP%/*} dev gre-msk metric 100
ip route replace $MAIL_SERVER via ${EKT_TUN_IP%/*} dev gre-ekt metric 200

# NAT для выхода в интернет. Не обязательно вставлять так как настройка НАТ проходит отдельно.
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

echo "Туннели на DC-RTR-1 настроены"
```

#### Для DC-RTR-2 (`/usr/local/bin/setup_tunnels_dc2.sh`):
```bash
#!/bin/bash

# ===== CONFIGURATION =====
# Основной туннель в Екатеринбург
EKT_REMOTE="10.8.8.2"    # YEKT-RTR внешний IP
EKT_LOCAL="10.8.8.1"     # DC-RTR-2 внешний IP
EKT_TUN_IP="192.168.200.1/30"

# Резервный туннель в Москву (через DC-RTR-1)
MSK_REMOTE="10.6.6.1"    # DC-RTR-1 внутренний IP
MSK_LOCAL="10.6.6.2"     # DC-RTR-2 внутренний IP
MSK_TUN_IP="192.168.201.1/30"

MAIL_SERVER="10.10.10.10" # IP почтового сервера
# ========================

# Настройка основного туннеля в Екатеринбург
ip tunnel add gre-ekt mode gre remote $EKT_REMOTE local $EKT_LOCAL ttl 255
ip link set gre-ekt up
ip addr add $EKT_TUN_IP dev gre-ekt

# Настройка резервного туннеля в Москву
ip tunnel add gre-msk mode gre remote $MSK_REMOTE local $MSK_LOCAL ttl 255
ip link set gre-msk up
ip addr add $MSK_TUN_IP dev gre-msk

# Включение маршрутизации
echo 1 > /proc/sys/net/ipv4/ip_forward

# Настройка маршрутов по умолчанию
ip route replace $MAIL_SERVER via ${EKT_TUN_IP%/*} dev gre-ekt metric 100
ip route replace $MAIL_SERVER via ${MSK_TUN_IP%/*} dev gre-msk metric 200

# NAT для выхода в интернет
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

echo "Туннели на DC-RTR-2 настроены"
```

### 2. Скрипты мониторинга и failover

#### Для MSK-RTR (`/usr/local/bin/failover_msk.sh`):
```bash
#!/bin/bash

# ===== CONFIGURATION =====
MAIN_GW="192.168.100.1"  # DC-RTR-1 туннель IP
BACKUP_GW="192.168.102.1" # DC-RTR-2 туннель IP
TEST_HOST="10.10.10.10"   # Почтовый сервер
CHECK_INTERVAL=10         # Интервал проверки в секундах
LOG_FILE="/var/log/gre_failover.log"
# ========================

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

log "Скрипт мониторинга запущен"

while true; do
    if ping -c 3 -I gre-dc1 $TEST_HOST &> /dev/null; then
        ip route replace default via $MAIN_GW dev gre-dc1
        log "Основной канал активен (через DC-RTR-1)"
    else
        ip route replace default via $BACKUP_GW dev gre-dc2
        log "Переключение на резервный канал (через DC-RTR-2)"
    fi
    sleep $CHECK_INTERVAL
done
```

#### Для YEKT-RTR (`/usr/local/bin/failover_yekt.sh`):
```bash
#!/bin/bash

# ===== CONFIGURATION =====
MAIN_GW="192.168.200.1"  # DC-RTR-2 туннель IP
BACKUP_GW="192.168.202.1" # DC-RTR-1 туннель IP
TEST_HOST="10.10.10.10"   # Почтовый сервер
CHECK_INTERVAL=10         # Интервал проверки в секундах
LOG_FILE="/var/log/gre_failover.log"
# ========================

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

log "Скрипт мониторинга запущен"

while true; do
    if ping -c 3 -I gre-dc2 $TEST_HOST &> /dev/null; then
        ip route replace default via $MAIN_GW dev gre-dc2
        log "Основной канал активен (через DC-RTR-2)"
    else
        ip route replace default via $BACKUP_GW dev gre-dc1
        log "Переключение на резервный канал (через DC-RTR-1)"
    fi
    sleep $CHECK_INTERVAL
done
```

### 3. Скрипты для тестирования (для пользователя test)

#### disable_primary.sh:
```bash
#!/bin/bash

# Эмулирует отказ основного канала
ip link set gre-dc1 down
echo "Основной туннель отключен (gre-dc1)"
```

#### enable_primary.sh:
```bash
#!/bin/bash

# Восстанавливает основной канал
ip link set gre-dc1 up
echo "Основной туннель восстановлен (gre-dc1)"
```

### 4. IPSec настройка (общий шаблон для всех узлов)

`/etc/ipsec.conf`:
```
config setup
    charondebug="all"
    uniqueids=yes

conn %default
    ikelifetime=60m
    keylife=20m
    rekeymargin=3m
    keyingtries=1
    keyexchange=ikev2
    ike=aes256-sha256-modp2048!
    esp=aes256-sha256!
    authby=secret

conn gre-tunnel
    left=%any
    leftid=@LOCAL_ID
    leftsubnet=0.0.0.0/0
    right=%any
    rightid=@REMOTE_ID
    rightsubnet=0.0.0.0/0
    auto=start
```

`/etc/ipsec.secrets`:
```
@LOCAL_ID @REMOTE_ID : PSK "your_shared_secret_key"
```

### Инструкция по применению:
1. Замените все IP-адреса в CONFIGURATION секциях на ваши
2. Для IPSec замените LOCAL_ID, REMOTE_ID и your_shared_secret_key
3. Сделайте скрипты исполняемыми:
   ```bash
   chmod +x /usr/local/bin/*.sh
   ```
4. Настройте автозапуск через systemd или cron @reboot
5. Для тестирования используйте скрипты disable_primary.sh/enable_primary.sh

Все скрипты логируют свои действия, что упрощает диагностику проблем.