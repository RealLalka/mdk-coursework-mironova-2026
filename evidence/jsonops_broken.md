# Протокол: jsonops_broken

Дата: 2026-11-08T19:50:51.689255+03:00

Команда: `/LoL/.scratch/mdk-coursework/venv/bin/python /LoL/.logs/mdk-coursework/verification-final/json_operations/test_02_valid.py`

Ожидался код 1, получен 1.

```text
Traceback (most recent call last):
  File "/LoL/.logs/mdk-coursework/verification-final/json_operations/test_02_valid.py", line 3, in <module>
    read("user.json")
    ~~~~^^^^^^^^^^^^^
  File "/LoL/.logs/mdk-coursework/verification-final/json_operations/storage.py", line 9, in read
    return json.loads((ROOT / name).read_text(encoding="utf-8"))
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/json/__init__.py", line 352, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "/usr/lib/python3.14/json/decoder.py", line 345, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/json/decoder.py", line 361, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 17 (char 16)

```
