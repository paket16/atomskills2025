## Шифрование

Перед настройкой установить strongswan `apt install strongswan`

Добавить ниже коды:

### Для DC-RTR-1
Защита туннеля в Москву
```
conn vpn-gre-msk
    auto=start
    type=tunnel
    authby=secret
    left=200.100.100.20
    right=188.121.90.2
    leftsubnet=0.0.0.0/0
    rightsubnet=0.0.0.0/0
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256
```

Защита туннеля в Екатеринбург
```
conn vpn-gre-ekt
    auto=start
    type=tunnel
    authby=secret
    left=200.100.100.20
    right=88.8.8.27
    leftsubnet=0.0.0.0/0
    rightsubnet=0.0.0.0/0
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256
```

### Для DC-RTR-2
Защита туннеля в Москву
```
conn vpn-gre-msk
    auto=start
    type=tunnel
    authby=secret
    left=100.200.100.20
    right=188.121.90.2
    leftsubnet=0.0.0.0/0
    rightsubnet=0.0.0.0/0
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256
```

Защита туннеля в Екатеринбург
```
conn vpn-gre-ekt
    auto=start
    type=tunnel
    authby=secret
    left=100.200.100.20
    right=88.8.8.27
    leftsubnet=0.0.0.0/0
    rightsubnet=0.0.0.0/0
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256
```

### Для MSK-RTR
Защита туннеля в DC-1
```
conn vpn-gre-dc1
    auto=start
    type=tunnel
    authby=secret
    left=188.121.90.2
    right=200.100.100.20
    leftsubnet=0.0.0.0/0
    rightsubnet=0.0.0.0/0
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256
```

Защита туннеля в DC-2
```
conn vpn-gre-dc2
    auto=start
    type=tunnel
    authby=secret
    left=188.121.90.2
    right=100.200.100.20
    leftsubnet=0.0.0.0/0
    rightsubnet=0.0.0.0/0
    leftprotoport=gre
    rightprotoport=gre
    ike=aes128-sha256-modp3072
    esp=aes128-sha256
```