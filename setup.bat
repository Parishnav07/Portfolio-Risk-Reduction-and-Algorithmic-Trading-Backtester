@echo off
REM Portfolio Risk Reduction - Setup Script for Windows

echo ==================================================
echo Portfolio Risk Reduction - Setup
echo ==================================================

REM Check Python version
echo.
echo Checking Python version...
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file
echo.
echo Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo Created .env file
    echo Please edit .env and add your Gemini API key
) else (
    echo .env file already exists
)

REM Create directories
echo.
echo Creating output directory...
if not exist output mkdir output
if not exist sample_data mkdir sample_data

REM Generate sample data
echo.
echo Generating sample data...
python generate_sample_data.py

echo.
echo ==================================================
echo Setup Complete!
echo ==================================================
echo.
echo Next steps:
echo   1. Edit .env file and add your Gemini API key
echo   2. Run the web app: streamlit run app.py
echo   3. Or use CLI: python main.py sample_data\stock_data.csv
echo.
echo For detailed instructions, see README.md
echo For quick start, see QUICKSTART.md
echo.
pause
