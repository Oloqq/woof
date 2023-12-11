# Setup
### Venv
- nie skipujcie tworzenia venva zeby wersje mesy sie nie pomieszaly
- `python -m venv venv`
- `venv\Scripts\Activate.ps1` (za kazdym razem przy otwarciu nowego terminala)
- `pip install -r requirements.txt`
nie przejmujcie sie tym warningiem
```
WARNING: The candidate selected for download or install is a yanked version: 'executing' candidate (version 2.0.0 at https://files.pythonhosted.org/packages/bb/3f/748594706233e45fd0e6fb57a2fbfe572485009c52b19919d161a0ae5d52/executing-2.0.0-py2.py3-none-any.whl (from https://pypi.org/simple/executing/))
Reason for being yanked: Released 2.0.1 which is equivalent but added 'python_requires = >=3.5' so that pip install with Python 2 uses the previous version 1.2.0.
WARNING: The candidate selected for download or install is a yanked version: 'jupyter-client' candidate (version 8.5.0 at https://files.pythonhosted.org/packages/ab/1f/d93fd1d2bf75233134a4aa1f56186b3c1975932fbfb58322e8de2906ea3d/jupyter_client-8.5.0-py3-none-any.whl (from https://pypi.org/simple/jupyter-client/) (requires-python:>=3.8))
Reason for being yanked: Bug in kernel env update
```
### Mesa
uzywamy forka Mesy
- robienie gitowych submodulow jest uciazliwe wiec
- kod jest w `src/mesa*`
- licencja: musimy miec gdzies liste wprowadzonych zmian (TBD)

# Uruchamianie
`python src/sim_mesa.py`