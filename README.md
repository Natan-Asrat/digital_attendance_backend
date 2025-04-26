## Setup
- Create a python virtual environment: `python -m venv venv`.
- Activate virtual environment:
    
    **On Windows**
    
    ```bash
    call venv/scripts/activate
    ```
    **On macOS/Linux**

    ```bash
    source venv/bin/activate
    ```
    
- Install dependencies: `pip install -r requirements.txt`.
- Create a `.env` file in `core` directory and add your environment variables.
    - Add `DEBUG` variable and set it to `true` if you are in debugging mode or `false` if you are in production.
    - **Debug**:
        ```
        DEBUG=true
        ```
    - **Production**:
        ```
        DEBUG=false
        ```
- Migrate to create database with `python manage.py migrate`
- Check everything works with `python manage.py runserver`