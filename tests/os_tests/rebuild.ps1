# ./rebuild.ps1  # careful - usually needs to be run twice

Remove-Item -path ./venv -recurse
# virtualenv venv -- with Python 3.8, venv works; on 3.10, python -m pip install ok
python -m venv venv
venv\Scripts\activate
echo "python -m pip install -r requirements.txt"
echo "python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ApiLogicServer==5.02.10"
echo "python -m pip install ApiLogicServer"
