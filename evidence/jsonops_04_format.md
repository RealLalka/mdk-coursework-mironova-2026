# Протокол: jsonops_04_format

Дата: 2026-11-08T19:50:50.962917+03:00

Команда: `/LoL/.scratch/mdk-coursework/venv/bin/python /LoL/.logs/mdk-coursework/verification-final/json_operations/04_format.py`

Ожидался код 0, получен 0.

```text
Компактно: {"id":1,"name":"Иван","email":"ivan@mail.ru","age":25,"active":true,"roles":["admin","user"]}
Отступы: {
  "id": 1,
  "name": "Иван",
  "email": "ivan@mail.ru",
  "age": 25,
  "active": true,
  "roles": [
    "admin",
    "user"
  ]
}
ASCII: {"id": 1, "name": "\u0418\u0432\u0430\u043d", "email": "ivan@mail.ru", "age": 25, "active": true, "roles": ["admin", "user"]}
Сортировка: {"active": true, "age": 25, "email": "ivan@mail.ru", "id": 1, "name": "Иван", "roles": ["admin", "user"]}

```
