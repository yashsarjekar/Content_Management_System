# Content_Management_System

## 1. Steps to get project setup and in running condition 
### Clone the Project 
```bash
git clone https://github.com/yashsarjekar/Content_Management_System.git
```
### Run Virtual Environment, by running this commend virtual environment will install and it will run.
```bash
pipenv shell
```
### Install Requirements
```bash
pip install -r requirements.txt
```
### Move to cms folder
 ```bash
 cd cms
 ```
 ### Makemigrations
 ```bash
 python manage.py makemigrations
 ```
 ### Migrate
 ```bash
 python manage.py migrate
 ```
 ### Createsuperuser provide Email,Password,Full name,Phone,Pincode
 ```bash
 python manage.py createsuperuser
 ```
### Run Django Server
```bash
python manage.py runserver
```
## 2. Restful API Structure
Restfull API Documentation:
Here please refer the Postman Documentation for working of this api.
Refer this Documentation while accessing this API.
Open New Tab in Google Chrome.
past the url.
https://documenter.getpostman.com/view/6268111/TW6tL9j7 

## 4. Conclusion 
### Hence we went through the process of creating a RESTful API using Django REST Framework.
