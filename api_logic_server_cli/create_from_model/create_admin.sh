echo on
echo 'Creating Admin Tables'

cd /Users/val/dev/servers/classicmodels/
export PYTHONPATH="/Users/val/dev/servers/classicmodels/"
source venv/bin/activate
cd ui/basic_web_app
export FLASK_APP=app
flask fab create-admin --username=admin --firstname="AdminFirst" --lastname=AdminLast --email=admin@apilogicserver.com --password=p
