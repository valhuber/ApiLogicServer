echo on
echo 'Creating Admin Tables'

cd /Users/val/dev/servers/classicmodels/
export PYTHONPATH="/Users/val/dev/servers/classicmodels/"
FILE=venv/bin/activate
if test -f "$FILE"; then
  echo "$FILE exists, so activate"
  source venv/bin/activate
else
  echo "$FILE does not exist, so using existing Python env (e.g., docker, ApiLogicServer"
fi
cd /Users/val/dev/servers/classicmodels//ui/basic_web_app
export FLASK_APP=app
flask fab create-admin --username=admin --firstname="AdminFirst" --lastname=AdminLast --email=admin@apilogicserver.com --password=p
