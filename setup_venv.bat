@echo off

:: Create virtual environment
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate

:: Install requirements
if exist requirements.txt (
    pip install -r requirements.txt
)

echo Virtual environment setup and activated.
