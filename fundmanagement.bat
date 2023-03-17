cd /d %~dp0

REM 仮想環境を有効化
call .\.venv\Scripts\activate.bat >> fundmanagement.log

REM Python実行
python main.py >> fundmanagement.log

REM 仮想環境を無効化
CALL .\.venv\Scripts\deactivate.bat >> fundmanagement.log