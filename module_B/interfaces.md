# На всех устройствах, указанных на топологии, создайте и настройте L3-адреса.

 Чтобы поднять сетевой сервис
 ```
 systemctl start networking.service
 systemctl restart networking.service

 #Настройка
 nano /etc/network/interfaces
 ```

ВАЖНО Оконечные устройства не пингуют 77.88.8.8 почему-то

## YEKT

### YEKT BILLING
```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.2.100/24
gateway 192.168.2.1
```

### YEKT DB
```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.2.150/24
gateway 192.168.2.1
```

### YEKT WORKER
```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 192.168.2.200/24
gateway 192.168.2.1
```

=====================================================

## MSK

### MSK WORKER and MSK-ADMINPC


```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

auto eth0
iface eth0 inet dhcp
```

### MSK GITLAB и MSK-DC
Убрать настроенный интерфейс и заменить на:

```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

auto enp1s0
iface enp1s0 inet static
address 192.168.1.3/24
gateway 192.168.1.1
```

### DC STORAGE

```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

auto enp1s0
allow-hotplug enp1s0
iface enp1s0 inet static
address 10.15.10.150/24
gateway 10.15.10.1
```

### DC MAILSERVER
Убрать настроенный интерфейс и заменить на:

```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

auto enp1s0
iface enp1s0 inet static
address 10.15.10.100/24
gateway 10.15.10.1
```