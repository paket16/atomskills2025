## DC


DC STORAGE и DC MAILSERVER не пингуют 77.88.8.8 !!!

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