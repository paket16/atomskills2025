## Шифрование

Команды для применения:
```bash
ipsec start
ipsec restart
ipsec status vpn-gre-ekt
```

Перед настройкой установить strongswan `apt install strongswan`

Добавить ниже коды (Важно не забывать про табы!!!):

### Для DC-RTR-1
Защита туннеля в Москву и Екатеринбург
```ini
conn vpn-gre-msk
    auto=start
    type=tunnel
    authby=secret
    left=200.100.100.20
    right=188.121.90.2
    leftsubnet=10.15.10.0/24
    rightsubnet=192.168.2.0/24
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256

conn vpn-gre-ekt
    auto=start
    type=tunnel
    authby=secret
    left=200.100.100.20
    right=88.8.8.27
    leftsubnet=10.15.10.0/24
    rightsubnet=192.168.1.0/24
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256
```

Для файла `/etc/ipsec.secrets`:
```ini
200.100.100.20 188.121.90.2 : PSK "P@ssw0rd"
200.100.100.20 88.8.8.27 : PSK "P@ssw0rd"
```

### Для DC-RTR-2
Защита туннеля в Москву и Екатеринбург
```ini
conn vpn-gre-msk
    auto=start
    type=tunnel
    authby=secret
    left=100.200.100.20
    right=188.121.90.2
    leftsubnet=10.15.10.0/24
    rightsubnet=192.168.1.0/24
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256

conn vpn-gre-ekt
    auto=start
    type=tunnel
    authby=secret
    left=100.200.100.20
    right=88.8.8.27
    leftsubnet=10.15.10.0/24
    rightsubnet=192.168.2.0/24
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256
```

Для файла `/etc/ipsec.secrets`:
```ini
100.200.100.20 188.121.90.2 : PSK "P@ssw0rd"
100.200.100.20 88.8.8.27 : PSK "P@ssw0rd"
```

### Для MSK-RTR
Защита туннеля в DC-1 и DC-2
```ini
conn vpn-gre-dc1
    auto=start
    type=tunnel
    authby=secret
    left=188.121.90.2
    right=200.100.100.20
    leftsubnet=192.168.1.0/24
    rightsubnet=10.15.10.0/24
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256

conn vpn-gre-dc2
    auto=start
    type=tunnel
    authby=secret
    left=188.121.90.2
    right=100.200.100.20
    leftsubnet=192.168.1.0/24
    rightsubnet=10.15.10.0/24
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256
```

Для файла `/etc/ipsec.secrets`:
```ini
188.121.90.2 100.200.100.20 : PSK "P@ssw0rd"
188.121.90.2 200.100.100.20 : PSK "P@ssw0rd"
```

### Для YEKT-RTR
Защита туннеля в DC-1 и DC-2
```ini
conn vpn-gre-dc1
    auto=start
    type=tunnel
    authby=secret
    left=88.8.8.27
    right=200.100.100.20
    leftsubnet=192.168.2.0/24
    rightsubnet=10.15.10.0/24
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256

conn vpn-gre-dc2
    auto=start
    type=tunnel
    authby=secret
    left=88.8.8.27
    right=100.200.100.20
    leftsubnet=192.168.2.0/24
    rightsubnet=10.15.10.0/24
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256
```

Для файла `/etc/ipsec.secrets`:
```ini
88.8.8.27 100.200.100.20 : PSK "P@ssw0rd"
88.8.8.27 200.100.100.20 : PSK "P@ssw0rd"
```