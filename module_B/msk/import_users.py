import csv
from ipalib import api

# Инициализация FreeIPA API
api.bootstrap(context='cli')
api.finalize()
api.Backend.rpcclient.connect()

def group_exists(group_name):
    """Проверяет, существует ли группа в FreeIPA"""
    try:
        api.Command.group_show(group_name)
        return True
    except Exception:
        return False

def create_group(group_name):
    """Создаёт новую группу в FreeIPA"""
    try:
        api.Command.group_add(group_name)
        print(f"Группа {group_name} успешно создана")
        return True
    except Exception as e:
        print(f"Ошибка при создании группы {group_name}: {str(e)}")
        return False

def import_users_from_csv(csv_file):
    """
    Импорт пользователей из CSV файла в FreeIPA
    
    Формат CSV: Lastname,FirstName,Groups
    Логин: фамилия пользователя
    Пароль: P@ssw0rd (без требования смены)
    """
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row in reader:
            if len(row) < 3:
                continue
                
            lastname, firstname, groups = row[0], row[1], row[2]
            login = lastname.lower()  # Используем фамилию как логин
            
            # Группы могут быть разделены запятыми или другими символами
            group_list = [g.strip() for g in groups.split(',') if g.strip()]
            
            try:
                # Создаем пользователя
                api.Command.user_add(
                    login,
                    givenname=firstname,
                    sn=lastname,
                    userpassword='P@ssw0rd',
                    krbpasswordexpiration=None,  # Пароль не требует смены
                    random=False
                )
                print(f"Пользователь {login} успешно создан")
                
                # Добавляем пользователя в группы
                for group in group_list:
                    try:
                        # Проверяем существование группы и создаём при необходимости
                        if not group_exists(group):
                            if create_group(group):
                                api.Command.group_add_member(group, user=login)
                                print(f"Пользователь {login} добавлен в группу {group}")
                        else:
                            api.Command.group_add_member(group, user=login)
                            print(f"Пользователь {login} добавлен в группу {group}")
                    except Exception as e:
                        print(f"Ошибка при добавлении в группу {group}: {str(e)}")
                        
            except Exception as e:
                print(f"Ошибка при создании пользователя {login}: {str(e)}")

if __name__ == '__main__':
    csv_file = input("Введите путь к CSV файлу: ")
    import_users_from_csv(csv_file)