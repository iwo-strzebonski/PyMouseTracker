# PyMouseTracker

Python Mouse Path renderer  
Created using `Python 3.10`, `turtle` and `pynput`

## Create executable

### Windows (EXE)

```cmd
pyinstaller --onefile PyMouseTracker.py
```

### Linux (ELF)

```sh
pyinstaller --onefile --hidden-import=pynput.keyboard._xorg --hidden-import=pynput.mouse._xorg PyMouseTracker.py
```
