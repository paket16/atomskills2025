# Команды для каждого роутера
## 2.1. DC-RTR-1 (IP: 10.15.10.3)
```
configure terminal
router ospf 1
 router-id 10.15.10.3
 passive-interface default
 no passive-interface Tunnel0
 exit
interface Tunnel0
 ip ospf authentication
 ip ospf authentication-key C00lCompanY
 exit
router ospf 1
 network 10.8.0.0 0.0.0.255 area 0
 exit
```
## 2.2. DC-RTR-2 (IP: 10.15.10.2)
```
configure terminal
router ospf 1
 router-id 10.15.10.2
 passive-interface default
 no passive-interface Tunnel0
 exit
interface Tunnel0
 ip ospf authentication
 ip ospf authentication-key C00lCompanY
 exit
router ospf 1
 network 10.8.0.0 0.0.0.255 area 0
 exit
```
## 2.3. MSK-RTR (IP: 192.168.1.0)
```
configure terminal
router ospf 1
 router-id 192.168.1.1
 passive-interface default
 no passive-interface Tunnel0
 exit
interface Tunnel0
 ip ospf authentication
 ip ospf authentication-key C00lCompanY
 exit
router ospf 1
 network 10.8.0.0 0.0.0.255 area 0
 exit
```
## 2.4. YEKT-RTR (IP: 192.168.2.1)
```
configure terminal
router ospf 1
 router-id 192.168.2.1
 passive-interface default
 no passive-interface Tunnel0
 exit
interface Tunnel0
 ip ospf authentication
 ip ospf authentication-key C00lCompanY
 exit
router ospf 1
 network 10.8.0.0 0.0.0.255 area 0
 exit
```

## Проверка соседей(работоспособности)
`show ip ospf neighbor`