Установка.

Клонировать репозиторий и перейти в его папку в командной строке:

```bash
git clone https://github.com/netsky_29/api_final_yatube
```

```bash 
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```bash 
python -m venv venv
```

Для *nix-систем:

```bash 
source venv/bin/activate
```

Для windows-систем:

```bash 
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash 
python -m pip install --upgrade pip
pip install -r requirements.txt
```