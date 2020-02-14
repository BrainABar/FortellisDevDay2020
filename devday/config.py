import json

# create file if not already created with twilio credentials
with open('/etc/config.json') as config_file:
    config = json.load(config_file)


class Config:

    TWILIO_ACCOUNT_SID = config.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = config.get('TWILIO_AUTH_TOKEN')
    TWILIO_NUMBER = config.get('TWILIO_NUMBER')
