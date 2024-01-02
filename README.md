## Run
```bash
uvicorn src.main:app --env-file .env --host 0.0.0.0 
```

## venv
```bash
# to init
pip install virtualenv 
python -m venv venv

# to run
source venv/bin/activate     # linux/mac
venv/Scripts/activate.bat    # In CMD
venv/Scripts/Activate.ps1    # In Powershell

# to deactivate 
deactivate
```

