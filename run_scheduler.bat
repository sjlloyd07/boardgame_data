@echo off

set original_dir="C:\Users\steve\project_repos\boardgame_data"
set venv_root_dir="C:\Users\steve\project_repos\boardgame_data\.venv"
::cd %venv_root_dir%
cd %original_dir%
call %venv_root_dir%\Scripts\activate.bat

python main.py

call %venv_root_dir%\Scripts\deactivate.bat
cd %original_dir%

exit
