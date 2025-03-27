```

#!/bin/bash

# Проверка, выполняется ли скрипт от root
if [[ $EUID -ne 0 ]]; then
   echo "Этот скрипт должен выполняться от root" 
   exit 1
fi

# Проверяем, есть ли уже правило в sudoers
if sudo grep -q "^%Admin ALL=(ALL) NOPASSWD:ALL" /etc/sudoers; then
    echo "Правило уже существует в sudoers."
else
    # Добавляем правило в sudoers
    echo "%Admin ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers > /dev/null
    echo "Правило добавлено в sudoers."
fi


```

Запускаем на MSK-ADMINPC