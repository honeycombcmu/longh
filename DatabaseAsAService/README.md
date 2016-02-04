Create a virtual environment venv
```
virtual venv
```

Enter the virtual environment venv
```
. venv/bin/activate
```

Install the packages from configuration file requirements.txt
```
pip install -r requirements.txt
```

Create a dataset from the Python shell
```
from app import init_db
init_db()
```

Run the appliation locally
```
python app.py
```

Quit the virtual environment venv
```
deactivate
```
