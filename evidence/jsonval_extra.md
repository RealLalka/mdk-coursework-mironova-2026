# Протокол: jsonval_extra

Дата: 2026-11-08T19:50:58.323471+03:00

Команда: `bash /LoL/33_mine/mdk-coursework-2026/testing/json_validation/run_all.sh`

Ожидался код 1, получен 1.

```text
2026-11-08 19:50:57 FAIL: JSON email_format
TOTAL=1 PASS=0 FAIL=1
2026-11-08 19:50:57 PASS: UTF-8 broken.json
2026-11-08 19:50:57 PASS: UTF-8 config.json
2026-11-08 19:50:57 PASS: UTF-8 orders.json
2026-11-08 19:50:57 PASS: UTF-8 products.json
2026-11-08 19:50:57 PASS: UTF-8 users.json
TOTAL=5 PASS=5 FAIL=0
2026-11-08 19:50:57 PASS: users.json существует
2026-11-08 19:50:57 PASS: config.json существует
TOTAL=2 PASS=2 FAIL=0
2026-11-08 19:50:57 PASS: JSON fields
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:57 PASS: jq: синтаксис
2026-11-08 19:50:57 PASS: jq: 3 пользователя
2026-11-08 19:50:57 PASS: jq: порт 8080
TOTAL=3 PASS=3 FAIL=0
2026-11-08 19:50:57 FAIL: JSON no_extra_fields
TOTAL=1 PASS=0 FAIL=1
2026-11-08 19:50:57 PASS: JSON orders
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:57 PASS: JSON products
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:57 PASS: JSON ranges
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:57 PASS: JSON schema
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:58 PASS: JSON types
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:58 FAIL: JSON unique_ids
TOTAL=1 PASS=0 FAIL=1
2026-11-08 19:50:58 FAIL: JSON users
TOTAL=1 PASS=0 FAIL=1
2026-11-08 19:50:58 PASS: users.json синтаксически корректен
2026-11-08 19:50:58 PASS: broken.json отклонён
TOTAL=2 PASS=2 FAIL=0

```
