<p align="center">
  <h1><b>S_QUANT_PROD</b></h1>
  <br>
  <h2><b>INTERNAL USE ONLY</b></h2>
</p>

### Git Initialization
```sh
this is for the repo --> https://github.com/01jeet/s_quant_prod.git

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/01jeet/s_quant_prod.git
git push -u origin main


if fails use this
git push --force -u origin main

```

### Create new folders
    ```sh
    create new folders
    New-Item -ItemType Directory -Name services
    New-Item -ItemType File -Path services/__init__.py
    ```
    
### Clean up Python caches and temporary tool folders
```sh

# 1. Clean up Python caches and temporary tool folders
Write-Host "Cleaning caches..." -ForegroundColor Cyan
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .pytest_cache, .mypy_cache, .ruff_cache, .coverage, htmlcov -ErrorAction SilentlyContinue

# 2. Force remove the virtual environment
Write-Host "Removing virtual environment..." -ForegroundColor Cyan
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

# 3. Clear uv global cache
Write-Host "Clearing uv cache..." -ForegroundColor Cyan
uv cache clean

# 4. Recreate and Sync (The 'Fresh Start')
Write-Host "Recreating environment..." -ForegroundColor Cyan
uv venv
uv sync

Write-Host "Success! Environment is clean and synced." -ForegroundColor Green
#end

```

### A Small test
```sh
  
  uv run ruff check .
  uv run ruff check . --fix
  uv run ruff format .
  uv run pylint .
  uv run pytest

```
