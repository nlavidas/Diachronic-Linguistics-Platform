@echo off
echo ========================================
echo CORPUS STATUS CHECK
echo ========================================
echo.
python LAPTOP_SYNC_UTILS.py status
echo.
echo ----------------------------------------
echo CHECKING DATABASE STATUS:
echo ----------------------------------------
python -c "import sqlite3; conn = sqlite3.connect('corpus_complete.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM texts'); print(f'Total texts collected: {cursor.fetchone()[0]}'); cursor.execute('SELECT COUNT(*) FROM texts WHERE processed = 1'); print(f'Texts processed: {cursor.fetchone()[0]}')"
echo.
pause