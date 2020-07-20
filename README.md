# SMS-Service #
Implementation of a SMS(Inbound/Outbound) service in Django with Basic authentication.
## Dependencies ##
    -Python3
    -Django

## Steps ##
1. Create and activate a Virtual environment:
    - sudo apt-get install virtualenv
    - virtualenv -p python3 venv
    - source venv/bin/activate
2. Clone git repo
    - git clone https://github.com/pratyushkhatait/sms-service-django.git
3. Install requirements.txt
    - pip install -r requirements.txt
4. Django runserver
    - python manage.py runserver
5. Hit Inbound SMS API
    - curl -X POST \
  http://127.0.0.1:8000/sms-service/inbound/sms/ \
  -H 'Authorization: Basic cGxpdm8xOjIwUzBLUE5PSU0=' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
	"_from": "4924195509100",
	"_to": "4924195509029",
	"_text": "STOP\n"
}'
6. Hit Outbound SMS API
    - curl -X POST \
  http://127.0.0.1:8000/sms-service/outbound/sms/ \
  -H 'Authorization: Basic cGxpdm8xOjIwUzBLUE5PSU0=' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache,no-cache' \
  -d '{
	"_from": "441224980086",
	"_to": "4924195509198",
	"_text": "Hello"
}'
