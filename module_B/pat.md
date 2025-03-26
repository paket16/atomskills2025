# NAT
`nano /etc/nftables.conf`

## Дописать снизу на всех роутерах (на некоторых может быть уже настроено)
```
table ip nat{
    chain postruoting{
    type nat hook postrouting priority 0;
    ip saddr 0.0.0.0/0 oifname "enp1s0" counter masquerade;
    }
}
```

## Включить таблицу
`systemctl enable nftables`

## Применить настроенный nat(перезагрузка сети не обязательна)
`nft -f /etc/nftables.conf`

## Включение поддержки маршрутизации и перессылки пакетов 
``` echo net.ipv4.ip_forward=1 > /etc/sysctl.conf
sysctl -p
```

## Проверка пингом с компов
` ping 77.88.8.8 `