# Настройки для всех кроме DC-STORAGE
```
# Создаем пользователя cod_admin
sudo useradd -m -s /bin/bash cod_admin

# Настраиваем каталог .ssh и права
sudo mkdir -p /home/cod_admin/.ssh
sudo chmod 700 /home/cod_admin/.ssh
sudo chown cod_admin:cod_admin /home/cod_admin/.ssh

# Копируем публичный ключ с DC-STORAGE (выполнить на DC-STORAGE)
scp /ssh_keys/<имя_устройства>_pub_key cod_admin@<IP_устройства>:/home/cod_admin/.ssh/authorized_keys

# На целевом устройстве: фиксируем права ключа
sudo chmod 600 /home/cod_admin/.ssh/authorized_keys
sudo chown cod_admin:cod_admin /home/cod_admin/.ssh/authorized_keys

# Разрешаем sudo без пароля
echo "cod_admin ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/cod_admin
sudo chmod 440 /etc/sudoers.d/cod_admin

# Настраиваем SSH только на внутреннем IPv4 (подставляем свой IP)
sudo sed -i '/^ListenAddress/d' /etc/ssh/sshd_config
echo "ListenAddress <внутренний_IP>" | sudo tee -a /etc/ssh/sshd_config
echo "PasswordAuthentication no" | sudo tee -a /etc/ssh/sshd_config
sudo systemctl restart sshd
```

# Настройки для DC-STORAGE
```
# Создаем пользователя cod_admin
sudo useradd -m -s /bin/bash cod_admin

# Удаляем все ключи из домашнего каталога (по ТЗ их не должно быть)
sudo rm -rf /home/cod_admin/.ssh

# Настраиваем sudo без пароля
echo "cod_admin ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/cod_admin
sudo chmod 440 /etc/sudoers.d/cod_admin

# Разрешаем парольный вход ТОЛЬКО для OpenConnect (подсеть 10.8.0.0/24 примерная)
sudo sed -i '/^ListenAddress/d' /etc/ssh/sshd_config
echo "ListenAddress 10.15.10.150" | sudo tee -a /etc/ssh/sshd_config
echo "Match Address 10.8.0.0/24" | sudo tee -a /etc/ssh/sshd_config
echo "    PasswordAuthentication yes" | sudo tee -a /etc/ssh/sshd_config
echo "Match all" | sudo tee -a /etc/ssh/sshd_config
echo "PasswordAuthentication no" | sudo tee -a /etc/ssh/sshd_config

# Устанавливаем пароль для cod_admin
echo "cod_admin:At0mSk1lls" | sudo chpasswd
sudo systemctl restart sshd

# Создаем каталог для ключей
sudo mkdir -p /ssh_keys
sudo chown cod_admin:cod_admin /ssh_keys
sudo chmod 700 /ssh_keys
```
# Генерация и распределение ключей (на DC-STORAGE)
## Генерируем ключи для каждого устрой-ва (на DC-STORAGE)

```
ssh-keygen -t ed25519 -f /ssh_keys/DC-MAILSERVER_key -C "cod_admin@DC-MAILSERVER"
ssh-keygen -t ed25519 -f /ssh_keys/DC-RTR-1_key -C "cod_admin@DC-RTR-1"
ssh-keygen -t ed25519 -f /ssh_keys/DC-RTR-2_key -C "cod_admin@DC-RTR-2"
ssh-keygen -t ed25519 -f /ssh_keys/MSK-GITLAB_key -C "cod_admin@MSK-GITLAB"
# ... и так для всех устройств
```
## Копируем ключи на устройства (пример для DC-MAILSERVER):
```
scp /ssh_keys/DC-MAILSERVER_key.pub cod_admin@10.15.10.100:/home/cod_admin/.ssh/authorized_keys

```
