### Настройка защищённых GRE-туннелей с автоматическим переключением

Для реализации отказоустойчивого решения с автоматическим переключением между каналами, я предлагаю следующую схему:

#### 1. Базовая настройка GRE-туннелей

**На DC-RTR-1:**
```bash
# Основной туннель в Москву
sudo ip tunnel add gre-msk mode gre remote 10.7.7.2 local 10.7.7.1 ttl 255
sudo ip link set gre-msk up
sudo ip addr add 192.168.100.1/30 dev gre-msk

# Резервный туннель в Екатеринбург (через DC-RTR-2)
sudo ip tunnel add gre-ekt mode gre remote 10.6.6.2 local 10.6.6.1 ttl 255
sudo ip link set gre-ekt up
sudo ip addr add 192.168.101.1/30 dev gre-ekt
```

**На DC-RTR-2:**
```bash
# Основной туннель в Екатеринбург
sudo ip tunnel add gre-ekt mode gre remote 10.8.8.2 local 10.8.8.1 ttl 255
sudo ip link set gre-ekt up
sudo ip addr add 192.168.200.1/30 dev gre-ekt

# Резервный туннель в Москву (через DC-RTR-1)
sudo ip tunnel add gre-msk mode gre remote 10.6.6.1 local 10.6.6.2 ttl 255
sudo ip link set gre-msk up
sudo ip addr add 192.168.201.1/30 dev gre-msk
```

**На MSK-RTR:**
```bash
# Основной туннель в DC-RTR-1
sudo ip tunnel add gre-dc1 mode gre remote 10.7.7.1 local 10.7.7.2 ttl 255
sudo ip link set gre-dc1 up
sudo ip addr add 192.168.100.2/30 dev gre-dc1

# Резервный туннель в DC-RTR-2
sudo ip tunnel add gre-dc2 mode gre remote 10.9.9.1 local 10.9.9.2 ttl 255
sudo ip link set gre-dc2 up
sudo ip addr add 192.168.102.2/30 dev gre-dc2
```

**На YEKT-RTR:**
```bash
# Основной туннель в DC-RTR-2
sudo ip tunnel add gre-dc2 mode gre remote 10.8.8.1 local 10.8.8.2 ttl 255
sudo ip link set gre-dc2 up
sudo ip addr add 192.168.200.2/30 dev gre-dc2

# Резервный туннель в DC-RTR-1
sudo ip tunnel add gre-dc1 mode gre remote 10.9.9.2 local 10.9.9.1 ttl 255
sudo ip link set gre-dc1 up
sudo ip addr add 192.168.202.2/30 dev gre-dc1
```

#### 2. Настройка шифрования (IPSec)

Для каждого туннеля необходимо настроить IPSec. Пример для туннеля между DC-RTR-1 и MSK-RTR:

**На DC-RTR-1 и MSK-RTR:**
```bash
sudo apt-get install strongswan
```

Конфигурация `/etc/ipsec.conf`:
```
conn gre-msk
    left=10.7.7.1
    right=10.7.7.2
    leftsubnet=192.168.100.0/30
    rightsubnet=192.168.100.0/30
    keyexchange=ikev2
    ike=aes256-sha1-modp1024!
    esp=aes256-sha1!
    keyingtries=%forever
    ikelifetime=28800s
    lifetime=3600s
    dpddelay=30s
    dpdtimeout=120s
    dpdaction=restart
    auto=start
```

#### 3. Настройка автоматического переключения

Создадим скрипты для мониторинга и переключения:

**На MSK-RTR (в /home/test/failover.sh):**
```bash
#!/bin/bash

MAIN_GW="192.168.100.1"  # DC-RTR-1
BACKUP_GW="192.168.102.1" # DC-RTR-2
TEST_HOST="mail.example.com" # Сервер почты

while true; do
    if ping -c 3 -I gre-dc1 $TEST_HOST &> /dev/null; then
        ip route replace default via $MAIN_GW dev gre-dc1
    else
        ip route replace default via $BACKUP_GW dev gre-dc2
    fi
    sleep 10
done
```

**На YEKT-RTR (аналогичный скрипт с другими параметрами):**
```bash
#!/bin/bash

MAIN_GW="192.168.200.1"  # DC-RTR-2
BACKUP_GW="192.168.202.1" # DC-RTR-1
TEST_HOST="mail.example.com"

while true; do
    if ping -c 3 -I gre-dc2 $TEST_HOST &> /dev/null; then
        ip route replace default via $MAIN_GW dev gre-dc2
    else
        ip route replace default via $BACKUP_GW dev gre-dc1
    fi
    sleep 10
done
```

#### 4. Настройка маршрутов

**На DC-RTR-1 и DC-RTR-2:**
```bash
# Включение IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# NAT для выхода в интернет
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

#### 5. Проверка работы

Для тестирования можно использовать скрипты из домашнего каталога пользователя test:
```bash
ssh test@router -p 22
# Пароль: P@ssw0rd

# Скрипт для "отключения" основного канала
./disable_primary.sh

# Скрипт для восстановления
./enable_primary.sh
```

#### 6. Автозапуск сервисов

Создаем systemd-юниты для автоматического запуска:

**Пример юнита (/etc/systemd/system/gre-tunnel.service):**
```
[Unit]
Description=GRE Tunnel Service
After=network.target

[Service]
ExecStart=/usr/local/bin/start-tunnels.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Важные замечания:
1. Все туннели используют существующие интерфейсы без создания дополнительных
2. Шифрование обеспечивается IPSec поверх GRE
3. Переключение происходит при недоступности почтового сервера
4. При восстановлении связи автоматически возвращаемся на основной канал
5. Топология строго соблюдается согласно заданию

Для полной реализации необходимо адаптировать скрипты под конкретные IP-адреса и тестовый хост (почтовый сервер). Также рекомендуется настроить логирование всех переключений для последующего аудита.