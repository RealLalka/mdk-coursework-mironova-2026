# Дополнительные эксперименты

```text
implicit: table persists without commit = True
explicit: table persists without commit = False
Flask debug reloader: Hello, Flask! -> Hello, Reload! PASS; isolated copy only
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:33669
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
127.0.0.1 - - [08/Nov/2026 19:45:25] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [08/Nov/2026 19:45:25] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [08/Nov/2026 19:45:25] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [08/Nov/2026 19:45:26] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [08/Nov/2026 19:45:26] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [08/Nov/2026 19:45:26] "GET / HTTP/1.1" 200 -
```
