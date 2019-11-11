：：We need to initialize all the environments when we start the new project.
@echo off
set INDEX_URL=https://mirrors.aliyun.com/pypi/simple
set URL_HOST=mirrors.aliyun.com
call %~dp0venv\Scripts\activate.bat
call easy_install -i %INDEX_URL% --upgrade pip
call pip install -i %INDEX_URL% --trusted-host %URL_HOST% tox pre-commit
call pre-commit install
call pip install -i %INDEX_URL% %URL_HOST% -r %~dp0requirements.txt -r %~dp0dev_requirements.txt
