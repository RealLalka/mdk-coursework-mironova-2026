# Протокол: stlc_public_example

Дата: 2026-11-08T19:50:50.235969+03:00

Команда: `bash /LoL/33_mine/mdk-coursework-2026/testing/stlc/run_stlc_tests.sh https://example.com`

Ожидался код 1, получен 1.

```text
PASS TC-01 / expected=200 actual=200
PASS TC-02 /not-found-xyz expected=404 actual=404
FAIL TC-03 /robots.txt expected=200 actual=404
FAIL TC-04 /favicon.ico expected=200 actual=404
FAIL TC-05 /redirect expected=302 actual=404
TOTAL=5 PASS=2 FAIL=3

```
