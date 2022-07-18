@echo off

echo Installing Python dependencies...
python -m pip install -r requirements.txt

echo Installing Node dependencies...
cd client
call npm i

echo Building client...
call npm run build

echo Deleting Node dependencies...
rm -r node_modules

echo Starting server...
cd ..
python -m server