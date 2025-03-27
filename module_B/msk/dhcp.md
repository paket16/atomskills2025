# НАСТРОЙКА ДЛЯ MSK-RTR
ВАЖНО!!! перед дальнейшей настройкой убедитесь что интерфейчы настроены согласно [interfaces](/module_B/interfaces.md)

## УСТАНОВКА DHCP-сервера
### Настраиваем зеркала 
`echo "77.88.8.8    repo.atomskills.ru" >> /etc/hosts/ # Доюавляем repo-miror `
` echo 'меняем deb.debian на на repo-mirror в /etc/apt/sources.list `


![sorces.list](../assets/sources.list.png)

### Настройка DHCP-сервера 

Меняем файл /etc/dhcp/dhcpd


![dhcpdp1](../assets/dhcpd.part1.png)
![dhcpdp2](../assets/dhcpd.part2.png) 

Далее выполняем `sudo dhclient` на обоих ПК