# Протокол: system_full

Дата: 2026-11-08T19:50:48.807873+03:00

Команда: `bash /LoL/33_mine/mdk-coursework-2026/testing/linux_system/run_all.sh`

Ожидался код 1, получен 1.

```text
NAME="Arch Linux"
PRETTY_NAME="Arch Linux"
ID=arch
BUILD_ID=rolling
ANSI_COLOR="38;2;23;147;209"
HOME_URL="https://archlinux.org/"
DOCUMENTATION_URL="https://wiki.archlinux.org/"
SUPPORT_URL="https://bbs.archlinux.org/"
BUG_REPORT_URL="https://gitlab.archlinux.org/groups/archlinux/-/issues"
PRIVACY_POLICY_URL="https://terms.archlinux.org/docs/privacy-policy/"
LOGO=archlinux-logo
6.6.87.2-microsoft-standard-WSL2
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdd       1007G  119G  838G  13% /
0.08 0.23 0.27 1/814 4084488
WARN: /etc/rosa-release отсутствует; это другой дистрибутив
PASS: Сервис sshd активен
WARN: Сервис crond не активен или systemd недоступен
WARN: Сервис NetworkManager не активен или systemd недоступен
SKIP: rpm -Va — на стенде нет RPM
OPEN: 127.0.0.1:22
CLOSED: 127.0.0.1:80
CLOSED: 127.0.0.1:443
CLOSED: 127.0.0.1:3306
CLOSED: 127.0.0.1:5432
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
Nov 06 01:05:10 DESKTOP-4R10HKQ kernel: misc dxg: dxgk: dxgkio_escape: Ioctl failed: -75
Nov 06 01:05:10 DESKTOP-4R10HKQ kernel: misc dxg: dxgk: dxgkio_escape: Ioctl failed: -75
Nov 06 01:05:10 DESKTOP-4R10HKQ kernel: misc dxg: dxgk: dxgkio_escape: Ioctl failed: -75
Nov 06 01:05:10 DESKTOP-4R10HKQ kernel: misc dxg: dxgk: dxgkio_escape: Ioctl failed: -75
Nov 06 01:05:15 DESKTOP-4R10HKQ kernel: misc dxg: dxgk: dxgkio_escape: Ioctl failed: -75
Nov 06 01:05:15 DESKTOP-4R10HKQ kernel: misc dxg: dxgk: dxgkio_escape: Ioctl failed: -75
Nov 06 07:41:05 DESKTOP-4R10HKQ unknown: WSL (246) ERROR: CheckConnection: getaddrinfo() failed: -5
Nov 06 12:50:50 DESKTOP-4R10HKQ unknown: WSL (246) ERROR: CheckConnection: getaddrinfo() failed: -5
Nov 07 15:38:37 DESKTOP-4R10HKQ sshd-session[2543105]: fatal: userauth_pubkey: parse publickey packet: incomplete message [preauth]
Nov 08 10:49:31 DESKTOP-4R10HKQ sshd-session[3553533]: fatal: userauth_pubkey: parse publickey packet: incomplete message [preauth]
SKIP: журналы secure/auth.log недоступны
577M	/var/log
2026-11-08 19:50:48 FAIL: Нет ERROR/FATAL в учебном журнале
TOTAL=1 PASS=0 FAIL=1
2026-11-08 19:50:48 PASS: Главная 200
2026-11-08 19:50:48 PASS: robots.txt 200
2026-11-08 19:50:48 PASS: Отсутствующий путь 404
2026-11-08 19:50:48 PASS: favicon.ico 200
2026-11-08 19:50:48 PASS: Время ответа меньше 2 секунд
response_time_seconds=0.001286
TOTAL=5 PASS=5 FAIL=0
requests=20 success=20 errors=0 duration_ms=192 mean_ms=9
2026-11-08 19:50:48 PASS: Все запросы успешны
TOTAL=1 PASS=1 FAIL=0

```
