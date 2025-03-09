@echo off
@REM Ppython -m nuitka --mingw64 --show-progress --remove-output --windows-console-mode=disable --lto=no --standalone --enable-plugin=pyside6 --include-module=Pycryptdome --include-data-dir=./img/=./img/ --include-data-files=./config.json=./config.json --output-dir=output main.py
chcp 65001
echo 目前暂未解决Nuitka与pycryptodomex之间的问题，暂不支持使用Nuitka打包
pause