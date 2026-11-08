# Протокол: postman_negative

Дата: 2026-11-08T19:51:05.957649+03:00

Команда: `/LoL/.scratch/mdk-coursework/node/node_modules/.bin/newman run /LoL/33_mine/mdk-coursework-2026/testing/postman/negative.postman_collection.json -e /LoL/33_mine/mdk-coursework-2026/testing/postman/test.postman_environment.json --timeout-request 15000`

Ожидался код 1, получен 1.

```text
newman

Намеренный отрицательный тест

→ Ожидаем неверный HTTP 404
  GET https://postman-echo.com/get [200 OK, 1.3kB, 269ms]
  1. HTTP 404 (намеренный сбой)
  ✓  Поле url — строка

┌─────────────────────────┬────────────────────┬───────────────────┐
│                         │           executed │            failed │
├─────────────────────────┼────────────────────┼───────────────────┤
│              iterations │                  1 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│                requests │                  1 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│            test-scripts │                  1 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│      prerequest-scripts │                  0 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│              assertions │                  2 │                 1 │
├─────────────────────────┴────────────────────┴───────────────────┤
│ total run duration: 317ms                                        │
├──────────────────────────────────────────────────────────────────┤
│ total data received: 277B (approx)                               │
├──────────────────────────────────────────────────────────────────┤
│ average response time: 269ms [min: 269ms, max: 269ms, s.d.: 0µs] │
└──────────────────────────────────────────────────────────────────┘

[31m  # [39m[31m failure        [39m[31m detail                                                [39m
[90m    [39m[90m                [39m[90m                                                       [39m
 1.  AssertionError  HTTP 404 (намеренный сбой)
                     expected response to have status code 404 but got 200
                     at assertion:0 in test-script
                     inside "Ожидаем неверный HTTP 404"

```
