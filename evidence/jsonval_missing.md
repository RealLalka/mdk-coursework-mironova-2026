# Протокол: jsonval_missing

Дата: 2026-11-08T19:50:55.163400+03:00

Команда: `bash /LoL/33_mine/mdk-coursework-2026/testing/json_validation/run_all.sh`

Ожидался код 1, получен 1.

```text
2026-11-08 19:50:54 PASS: JSON email_format
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:54 PASS: UTF-8 broken.json
2026-11-08 19:50:54 PASS: UTF-8 config.json
2026-11-08 19:50:54 PASS: UTF-8 orders.json
2026-11-08 19:50:54 PASS: UTF-8 products.json
2026-11-08 19:50:54 PASS: UTF-8 users.json
TOTAL=5 PASS=5 FAIL=0
2026-11-08 19:50:54 PASS: users.json существует
2026-11-08 19:50:54 PASS: config.json существует
TOTAL=2 PASS=2 FAIL=0
2026-11-08 19:50:54 FAIL: JSON fields
TOTAL=1 PASS=0 FAIL=1
2026-11-08 19:50:54 PASS: jq: синтаксис
2026-11-08 19:50:54 PASS: jq: 3 пользователя
2026-11-08 19:50:54 FAIL: jq: порт 8080
TOTAL=3 PASS=2 FAIL=1
2026-11-08 19:50:54 PASS: JSON no_extra_fields
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:54 PASS: JSON orders
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:54 PASS: JSON products
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:54 FAIL: JSON ranges
TOTAL=1 PASS=0 FAIL=1
2026-11-08 19:50:54 FAIL: JSON schema
TOTAL=1 PASS=0 FAIL=1
2026-11-08 19:50:54 FAIL: JSON types
TOTAL=1 PASS=0 FAIL=1
2026-11-08 19:50:54 PASS: JSON unique_ids
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:55 PASS: JSON users
TOTAL=1 PASS=1 FAIL=0
2026-11-08 19:50:55 PASS: users.json синтаксически корректен
2026-11-08 19:50:55 PASS: broken.json отклонён
TOTAL=2 PASS=2 FAIL=0

```
