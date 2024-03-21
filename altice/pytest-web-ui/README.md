# pytest-web-ui

## Install


Clone this repository using the following command

> ` git clone https://github.com/greearb/pytest-web-ui.git `

or you can download the zip file [here](https://github.com/greearb/pytest-web-ui/archive/refs/heads/main.zip).

## Usage


- ### Create a Virtual environment (venv as webui) and activate it

    > `python -m venv webui`


    > `source webui/bin/activate`


    > `source bin/activate`

- ### Install Requirements

    > `pip install -r requirements.txt`
    
    > pip install psycopg2-binary

    > pip install pytest-json-report

    > pip install pytest-html

    > pip install pytest-json

- ### Run Commands
    > `sudo apt install rabbitmq-server`
    
    > sudo apt install apache2

    > `sudo systemctl enable rabbitmq-server`
    
    > `sudo systemctl start rabbitmq-server`
    
    > `sudo systemctl status rabbitmq-server`
    
    > `/etc/init.d/apache2 start`
- ### Run the Server

    Open the project directory
    > `python manage.py makemigrations`

    > `python manage.py migrate`

    > `python manage.py runserver`
    
    In the other terminal
    
    > `celery -A pytest_web_ui worker --beat --scheduler django --loglevel=info`
    
    Open the Browser

    <http://127.0.0.1:8000/>

    login: tester1@candelatech.com

    password: Lanforge@123
