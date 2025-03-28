***
Реализуйте веб-сайт, на базе YEKT-RTR:
веб-сайт с поддержкой авторизации согласено таблице пин-кодов;
пользователь вводит свой уникальный ПИН-код (исходя из таблицы пин-кодов);
при переходе на корневую страницу сайта пользователю предлагается на выбор две ссылки:
    click here for admin;
    click here for worker.
после выбора нужной ссылки для пользователя запрашивается авторизация на сайте, пользователь наблюдает HTML-страницу:
    Если зашел как /admin, страница пишет - Hello Admins!
    Если зашел как /worker, страница пишет - Hello Workers!

Пин-код:

Пользователь 	пин-код

ssl_admin |	159753486
            
ssl_worker|	951753426
***

## Ответ AI

### **Реализация веб-сайта с авторизацией по пин-кодам**
Мы создадим веб-сайт на Flask с базовой авторизацией по пин-кодам.

---

### **1. Установка зависимостей**
На сервере **YEKT-RTR**:
```bash
sudo apt update && sudo apt install python3 python3-pip -y
pip3 install flask
```

---

### **2. Создание файлов проекта**
Создадим структуру:
```bash
mkdir -p /var/www/pin_auth && cd /var/www/pin_auth
touch app.py templates/index.html templates/admin.html templates/worker.html
```

---

### **3. Код сервера (app.py)**
```python
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Для работы сессий

# Таблица пин-кодов
PIN_CODES = {
    "159753486": "admin",
    "951753426": "worker"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pin = request.form.get("pin")
        if pin in PIN_CODES:
            session["role"] = PIN_CODES[pin]
            return redirect(url_for(PIN_CODES[pin]))
        return "Неверный PIN-код!", 403
    return render_template("index.html")

@app.route("/admin")
def admin():
    if session.get("role") == "admin":
        return render_template("admin.html")
    return redirect(url_for("index"))

@app.route("/worker")
def worker():
    if session.get("role") == "worker":
        return render_template("worker.html")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

---

### **4. HTML-шаблоны**
#### **Главная страница (templates/index.html)**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Enter PIN code</h2>
    <form method="POST">
        <input type="password" name="pin" required>
        <button type="submit">Submit</button>
    </form>
    <br>
    <a href="/admin">Click here for admin</a>
    <br>
    <a href="/worker">Click here for worker</a>
</body>
</html>
```

#### **Страница администратора (templates/admin.html)**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Admin</title>
</head>
<body>
    <h1>Hello Admins!</h1>
</body>
</html>
```

#### **Страница работника (templates/worker.html)**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Worker</title>
</head>
<body>
    <h1>Hello Workers!</h1>
</body>
</html>
```

---

### **5. Запуск сервера**
```bash
cd /var/www/pin_auth
python3 app.py
```
Теперь сайт доступен на **YEKT-RTR** 🚀