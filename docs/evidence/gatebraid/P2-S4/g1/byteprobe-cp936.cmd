@echo off
chcp 936 >NUL
set PYTHONDONTWRITEBYTECODE=1
C:\Python312\python.exe -B docs/evidence/gatebraid/P2-S4/g1/byteprobe.py report
echo ---TEXT-PATH---
C:\Python312\python.exe -B docs/evidence/gatebraid/P2-S4/g1/byteprobe.py text
echo ---BYTES-PATH---
C:\Python312\python.exe -B docs/evidence/gatebraid/P2-S4/g1/byteprobe.py bytes
