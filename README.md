# image_project
Python Django project to process images and videos for YouTube
# Setting Up a Django Project

### Prerequisites
- Python 3 installed on your system.
- Git installed (optional, for version control).

### Steps to Set Up a Django Project
https://github.com/JupyterJones/image_project/archive/refs/heads/main.zip
and unzip

or git clone https://github.com/JupyterJones/image_project.git
#### 1. Create and Activate a Virtual Environment
```bash

cd image_project
python3 -m venv venv
```
- **Activate the Environment**:
  - On Linux/macOS:
    ```bash
    source venv/bin/activate
    ```
  - On Windows:
    ```bash
    venv\Scripts\activate
    ```

#### 2. Install Django
```bash
pip install django
```
Verify installation:
```bash
django-admin --version
```

#### 3. Start a Django Project
```bash
django-admin startproject mysite .
```

Run the development server to verify:
```bash
python manage.py runserver
```
Visit: `http://127.0.0.1:8000/` to confirm setup.

#### 4. Create a `requirements.txt`
Generate dependencies:
```bash
pip freeze > requirements.txt
```
Example `requirements.txt`:
```
Django==4.2.5
asgiref==3.7.2
sqlparse==0.4.4
tzdata==2023.3
```

#### 5. Install Dependencies From `requirements.txt`
For future setups:
```bash
pip install -r requirements.txt
```

### Project Structure
```
my_django_project/
├── manage.py
├── mysite/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
├── venv/ (virtual environment files)
└── requirements.txt
```

### Next Steps
- Create an app: `python manage.py startapp myapp`
- Add the app to `INSTALLED_APPS` in `settings.py`.

For more details, visit the [Django documentation](https://docs.djangoproject.com/).

