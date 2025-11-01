@echo off
REM Script để kích hoạt virtual environment trên Windows CMD
REM Cách sử dụng: activate_venv.bat

echo === Kich hoat Virtual Environment ===

REM Kiểm tra venv đã tồn tại chưa
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment chua duoc tao!
    echo Dang tao virtual environment...
    python -m venv venv
)

REM Kích hoạt venv
echo Dang kich hoat virtual environment...
call venv\Scripts\activate.bat

if %ERRORLEVEL% EQU 0 (
    echo Virtual environment da duoc kich hoat!
    python --version
    echo.
    echo De thoat venv, go: deactivate
) else (
    echo Khong the kich hoat virtual environment!
)

