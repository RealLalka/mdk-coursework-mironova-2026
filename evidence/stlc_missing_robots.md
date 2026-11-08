# Протокол: stlc_missing_robots

Дата: 2026-11-08T19:50:49.464314+03:00

Команда: `bash /LoL/33_mine/mdk-coursework-2026/testing/stlc/run_stlc_tests.sh http://127.0.0.1:42089`

Ожидался код 1, получен 1.

```text
PASS TC-01 / expected=200 actual=200
PASS TC-02 /not-found-xyz expected=404 actual=404
FAIL TC-03 /robots.txt expected=200 actual=404
PASS TC-04 /favicon.ico expected=200 actual=200
PASS TC-05 /redirect expected=302 actual=302
TOTAL=5 PASS=4 FAIL=1

```
