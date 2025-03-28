*На сервере YEKT-RTR разверните подчиненный Центр сертификации:*

*Подпишите подчиненный сертификат вашим основном ЦС в городе Москва;
Каталог для центра сертификации - /sub/ca;
Имя центра сертификации - Yekaterinburg CA;
Остальные сведения наследуются с основного ЦС.*

## Ответ AI
### **Настройка подчиненного Центра сертификации (Yekaterinburg CA)**
Задание предполагает создание подчинённого CA и его интеграцию с основным московским CA.

---

## **1. Установка OpenSSL и инициализация каталога CA**
На сервере **YEKT-RTR**:
```bash
sudo apt update && sudo apt install openssl -y
sudo mkdir -p /sub/ca/{certs,crl,newcerts,private}
sudo chmod 700 /sub/ca/private
sudo touch /sub/ca/index.txt
echo 1000 | sudo tee /sub/ca/serial
```

Создадим конфигурацию CA:
```bash
sudo nano /sub/ca/openssl.cnf
```
Добавляем:
```ini
[ ca ]
default_ca = Yekaterinburg_CA

[ Yekaterinburg_CA ]
dir = /sub/ca
certs = $dir/certs
crl_dir = $dir/crl
database = $dir/index.txt
new_certs_dir = $dir/newcerts
certificate = $dir/certs/ca.crt
serial = $dir/serial
private_key = $dir/private/ca.key
default_days = 3650
default_md = sha256
policy = policy_any
email_in_dn = no

[ policy_any ]
countryName = supplied
stateOrProvinceName = supplied
localityName = supplied
organizationName = supplied
organizationalUnitName = optional
commonName = supplied
emailAddress = optional
```

---

## **2. Создание запроса на сертификат**
Генерируем закрытый ключ и CSR-запрос:
```bash
openssl genrsa -out /sub/ca/private/ca.key 4096
openssl req -new -key /sub/ca/private/ca.key -out /sub/ca/ca.csr -subj "/CN=Yekaterinburg CA"
```
Передаём `ca.csr` на сервер московского CA.

---

## **3. Подписываем сертификат в Москве**
На сервере **MSK-CA** (основной центр сертификации):
```bash
openssl ca -in /path/to/received/ca.csr -out /path/to/response/ca.crt -days 3650 -extensions v3_ca
```
Возвращаем `ca.crt` обратно на **YEKT-RTR**.

---

## **4. Завершаем настройку подчинённого CA**
На **YEKT-RTR**, размещаем подписанный сертификат:
```bash
sudo mv ca.crt /sub/ca/certs/
```
Готово! Теперь **Yekaterinburg CA** работает под основным московским CA. 🚀