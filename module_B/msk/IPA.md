# Настройка доменного контроллера
## Добавляем пользователей из csv 
## SCRIPT
Перед использованием: `kinit -p admin`
[python script](./import_users.py)
## Добавляем компы в домен 
ИЗменяем sources.list
sudo apt update 
sudo apt install astra-freeipa-client
!!!ОБЯЗАТЕЛЬНО ПРОВЕРЬТЕ HOSTNAME!!!
sudo astra-freeipa-client

вауля компы в домене!!)

