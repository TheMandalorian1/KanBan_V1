# to create virtualenv using windows command promt
- change directory `cd`+ project_folder path
- to create virtualenv `python3 -m venv .proj-env`
- to activate virtualenv `.proj-env\Scripts\activate.bat`

# to intall required packages-
- to install all packages `pip install -r requirements.txt`
# to run the application -
- `python main.py`

# Folder Structure
- `application` is where our application code is.
- `static` - default `static` files folder and has CSS files. 
- `static/images` has all the images.
- `templates` - Default flask templates folder
- `documents` has yaml file for API and project report pdf.


```
├── application
│   ├── api.py
│   ├── app.py
│   ├── __init__.py
│   ├── models.py
│   └── __pycache__
│       ├── __init__.cpython-310.pyc
│       ├── api.cpython-310.pyc
│       ├── app.cpython-310.pyc
│       └── models.cpython-310.pyc
|
├── addDB.sqlite3
├── main.py
├── readme.md
├── requirements.txt
|
├── static
│   ├── images
│   │   ├── img1.jpg
|   |   |
|   |
│   ├── style.css
|   ├── style1.css
|   └── styles.css
|
├── documents
│   ├── openapi.yaml
|   └── Project Report.pdf
|
└── templates
    ├── base.html
    ├── base1.html
    ├── cardadd.html
    ├── confirmc.html
    ├── confirml.html
    ├── dashboard.html
    ├── editc.html
    ├── elist.html
    ├── home.html
    ├── listadd.html
    ├── login.html
    ├── register.html
    └── summary.html
```