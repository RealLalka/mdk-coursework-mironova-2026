# Протокол: postman_positive

Дата: 2026-11-08T19:51:04.973492+03:00

Команда: `/LoL/.scratch/mdk-coursework/node/node_modules/.bin/newman run /LoL/33_mine/mdk-coursework-2026/testing/postman/homework.postman_collection.json -e /LoL/33_mine/mdk-coursework-2026/testing/postman/test.postman_environment.json --timeout-request 15000 --reporters cli,json --reporter-json-export /LoL/.logs/mdk-coursework/verification-final/postman-positive.json`

Ожидался код 0, получен 0.

```text
newman

Домашняя работа

→ Первый GET
  GET https://postman-echo.com/get [200 OK, 1.29kB, 277ms]
  ✓  HTTP 200
  ✓  Поле url — строка

→ GET с именем
  GET https://postman-echo.com/get?name=Анна [200 OK, 1.23kB, 262ms]
  ✓  HTTP 200
  ✓  Поле url — строка
  ✓  args.name совпадает с именем

┌─────────────────────────┬────────────────────┬───────────────────┐
│                         │           executed │            failed │
├─────────────────────────┼────────────────────┼───────────────────┤
│              iterations │                  1 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│                requests │                  2 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│            test-scripts │                  2 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│      prerequest-scripts │                  0 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│              assertions │                  5 │                 0 │
├─────────────────────────┴────────────────────┴───────────────────┤
│ total run duration: 607ms                                        │
├──────────────────────────────────────────────────────────────────┤
│ total data received: 1.03kB (approx)                             │
├──────────────────────────────────────────────────────────────────┤
│ average response time: 269ms [min: 262ms, max: 277ms, s.d.: 7ms] │
└──────────────────────────────────────────────────────────────────┘

```
