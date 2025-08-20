@echo off
echo ========================================
echo PREPARING TO SWITCH LAPTOPS
echo ========================================
echo.
echo This will:
echo 1. Save your current state
echo 2. Close all connections
echo 3. Prepare for safe Z: drive removal
echo.
python LAPTOP_SYNC_UTILS.py before
echo.
echo ✅ You can now safely remove Z: drive!
pause