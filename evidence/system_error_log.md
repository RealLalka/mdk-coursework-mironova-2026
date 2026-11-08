# Протокол: system_error_log

Дата: 2026-11-08T19:50:48.230462+03:00

Команда: `bash /LoL/33_mine/mdk-coursework-2026/testing/linux_system/log_check.sh`

Ожидался код 1, получен 1.

```text
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

```
