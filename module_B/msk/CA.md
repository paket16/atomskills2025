# Развертывание Основного Центра Сертификации (Root CA) на MSK-DC1

## Подготовка окружения

1. Установите необходимые пакеты:
```bash
sudo apt update
sudo apt install -y openssl
```

2. Создайте структуру каталогов:
```bash
sudo mkdir -p /root/ca/{certs,crl,newcerts,private,csr}
sudo chmod 700 /root/ca/private
sudo touch /root/ca/index.txt
echo 1000 | sudo tee /root/ca/serial
```

## Настройка OpenSSL

1. Создайте конфигурационный файл `/root/ca/openssl.cnf`:
```ini
[ ca ]
default_ca = CA_default

[ CA_default ]
dir               = /root/ca
certs             = $dir/certs
crl_dir           = $dir/crl
new_certs_dir     = $dir/newcerts
database          = $dir/index.txt
serial            = $dir/serial
RANDFILE          = $dir/private/.rand

private_key       = $dir/private/ca.key.pem
certificate       = $dir/certs/ca.cert.pem

name_opt          = ca_default
cert_opt          = ca_default
default_days      = 3650
default_crl_days  = 30
default_md        = sha256
preserve          = no
policy            = policy_strict

[ policy_strict ]
countryName             = match
stateOrProvinceName     = match
organizationName        = match
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[ req ]
default_bits        = 4096
distinguished_name  = req_distinguished_name
string_mask         = utf8only
default_md          = sha256
x509_extensions     = v3_ca

[ req_distinguished_name ]
countryName                     = Country Name (2 letter code)
countryName_default             = RU
countryName_min                 = 2
countryName_max                 = 2

stateOrProvinceName             = State or Province Name
stateOrProvinceName_default      = Московская

localityName                    = Locality Name
localityName_default            = Москва

0.organizationName              = Organization Name
0.organizationName_default      = Cool CA

organizationalUnitName          = Organizational Unit Name
organizationalUnitName_default  = Certificate Authority

commonName                      = Common Name
commonName_default              = Cool CA Root Certificate

emailAddress                    = Email Address
emailAddress_max                = 64

[ v3_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[ server_cert ]
basicConstraints = CA:FALSE
nsCertType = server
nsComment = "OpenSSL Generated Server Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
```

## Создание корневого сертификата

1. Создайте закрытый ключ CA:
```bash
sudo openssl genrsa -aes256 -out /root/ca/private/ca.key.pem 4096
sudo chmod 400 /root/ca/private/ca.key.pem
```

2. Создайте корневой сертификат:
```bash
sudo openssl req -config /root/ca/openssl.cnf \
      -key /root/ca/private/ca.key.pem \
      -new -x509 -days 7300 -sha256 -extensions v3_ca \
      -out /root/ca/certs/ca.cert.pem
```

3. Установите правильные разрешения:
```bash
sudo chmod 444 /root/ca/certs/ca.cert.pem
```

## Проверка сертификата

```bash
sudo openssl x509 -noout -text -in /root/ca/certs/ca.cert.pem
```

## Настройка доверия на всех компьютерах инфраструктуры

1. Экспортируйте сертификат в формате DER:
```bash
sudo openssl x509 -outform der -in /root/ca/certs/ca.cert.pem -out /root/ca/certs/ca.cert.der
```

2. Для добавления в доверенные на Windows-компьютерах:
```powershell
Import-Certificate -FilePath "\\MSK-DC1\ca\ca.cert.der" -CertStoreLocation Cert:\LocalMachine\Root
```

3. Для Linux-компьютеров:
```bash
sudo -i && cd /usr/local/share/ca-certificates/ && wget http://192.168.1.2/Cool_CA.crt &&  update-ca-certificates
```

## Настройка веб-сервисов на HTTPS

1. Для настройки веб-серверов (например, Apache):
```bash
sudo apt install -y apache2
sudo a2enmod ssl
```

2. Создайте сертификат для веб-сервера:
```bash
sudo openssl genrsa -out /etc/ssl/private/server.key 2048
sudo openssl req -new -key /etc/ssl/private/server.key -out /root/ca/csr/server.csr
sudo openssl ca -config /root/ca/openssl.cnf -extensions server_cert -days 375 -notext -md sha256 -in /root/ca/csr/server.csr -out /etc/ssl/certs/server.crt
```

3. Настройте Apache для использования HTTPS:
```bash
sudo nano /etc/apache2/sites-available/default-ssl.conf
```
Добавьте:
```apache
SSLEngine on
SSLCertificateFile /etc/ssl/certs/server.crt
SSLCertificateKeyFile /etc/ssl/private/server.key
SSLCACertificateFile /root/ca/certs/ca.cert.pem
```

## Настройка OpenConnect (ocserv)

1. Установите ocserv:
```bash
sudo apt install -y ocserv
```

2. Создайте сертификат для OpenConnect:
```bash
sudo openssl genrsa -out /etc/ocserv/server-key.pem 2048
sudo openssl req -new -key /etc/ocserv/server-key.pem -out /root/ca/csr/ocserv.csr
sudo openssl ca -config /root/ca/openssl.cnf -extensions server_cert -days 375 -notext -md sha256 -in /root/ca/csr/ocserv.csr -out /etc/ocserv/server-cert.pem
```

3. Настройте ocserv для использования HTTPS:
```bash
sudo nano /etc/ocserv/ocserv.conf
```
Укажите:
```ini
server-cert = /etc/ocserv/server-cert.pem
server-key = /etc/ocserv/server-key.pem
ca-cert = /root/ca/certs/ca.cert.pem
```

После выполнения этих шагов у вас будет полностью функционирующий центр сертификации, выпускающий доверенные сертификаты для всей инфраструктуры.