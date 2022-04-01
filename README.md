# Hunpress Deadcounter
Egy egyszerű python script segítségével statisztikát kaphatunk a magyar sajtó legnagyobb online portáljainak aktuális halálhír dömpingjéről.

### Környezet beállítása
```
git clone https://github.com/kaktusztea/hunpress_deadcounter.git
cd hunpress_deadcounter
python3 -m venv venv
source bin/activate
pip install --upgrade -i https://pypi.org/simple pip
pip install -i https://pypi.org/simple bs4 requests
```

### Script futtatása
```
./counter.py
```

### Script leállítása
Leállítás után a script legenerálja a statisztikai ábrákat.
```
CTRL + C
```
