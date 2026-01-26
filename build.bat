@echo off
set NEWSPAPER_RES="Python\Python313\Lib\site-packages\newspaper\resources 주소"

pyinstaller ^
  --onefile ^
  --windowed ^
  --noupx ^
  --runtime-tmpdir %TEMP% ^
  --add-data %NEWSPAPER_RES%;newspaper\resources ^
  --hidden-import utils ^
  main.py

pause