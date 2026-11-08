# Протокол: system_insecure_permissions

Дата: 2026-11-08T19:50:48.192556+03:00

Команда: `bash /LoL/33_mine/mdk-coursework-2026/testing/linux_system/integrity_check.sh`

Ожидался код 1, получен 1.

```text
644 root /etc/passwd
1fede5b6c5287a65477f821d2335e63a79b2ec1bf12dd69850f586b704513ba5  /etc/passwd
644 root /etc/group
342d9c4043953ce5c9efddfa9e34e0c2d8868f96fd182c33ecd880c61e0549f4  /etc/group
644 root /etc/hosts
fca6fb32ed9529aacbaf6103a9132a11e3172a8203c130b64a7b8a35daa576aa  /etc/hosts
644 root /etc/fstab
e54626e74ed8fee4173b62a545ab1c3a3a069e4217a0ee8fc398d9933e9c1696  /etc/fstab
440 root /etc/sudoers
ef8f58e8047b9308914150b8d0cabdd2120e4dfd7a4599b0f2d3d1e5cf4405aa  /etc/sudoers
2026-11-08 19:50:48 FAIL: Учебный конфиг не world-writable
TOTAL=1 PASS=0 FAIL=1

```
