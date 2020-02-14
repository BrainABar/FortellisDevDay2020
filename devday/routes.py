from flask import Flask, abort, request, jsonify
from devday import app, Swagger, Config
from devday.twiliohandler import TwilioHandler
import json

handler = TwilioHandler(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN, Config.TWILIO_NUMBER)
appointments = {}
msgcount = [0]


@app.route('/sms/', methods=['POST'])
def process_sms():
    msgcount[0] += 1

    if request.headers.get('X-Twilio-Signature'):
        body = request.form['Body']
        fromnumber = request.form['From']

        if 'ok' in body:
            customermessage = 'Thank you. We shall notify you once work is complete'
            handler.createmessage(customermessage, to=fromnumber)

        return '<Response></Response>'

    return '', 404


@app.route('/setappointment/', methods=['POST'])
def set_appointment():
    """
    Sets the appointment for the customer
    ---
    tags:
        - Set appointment endpoint
    parameters:
        -   name: name
            in: path
            type: string
            required: true
            description: The name of the customer
        -   name: time
            in: path
            type: string
            required: true
            description: Time of appointment as 'HHMM'
        -   name: number
            in: path
            type: string
            required: true
            description: Client's phone number
    :return:
    """
    if request.method == 'POST':
        customer = {}
        name = request.args['name']
        time = request.args['time']
        number = request.args['number']
        customer['id'] = len(appointments) + 1
        customer['name'] = name
        customer['time'] = time
        customer['number'] = number
        customer['car'] = '2010 Nissan Altima'
        customer['isComplete'] = False
        customer['workApproved'] = False
        customer['price'] = 1000
        customer['techName'] = 'Rebel Tech'
        customer['hasArrived'] = False
        customer['issue'] = 'Spark plug needs tightening'
        customer['custComment'] = 'Fix it'
        customer['techComment'] = 'Fixing your car'
        appointments[customer['id']] = json.dumps(customer)

        customermessage = '{}, you have an appointment at Rebel Shop at {}, for your {}'.format(name, time, customer['car'])

        handler.createmessage(customermessage, to=customer['number'])

        return json.dumps(customer)


@app.route('/getappointment/<int:task_id>', methods=['GET'])
def get_appointment(task_id):
    return appointments[task_id]


@app.route('/approveservice/<int:task_id>', methods=['POST'])
def approve_service(task_id):
    if task_id in appointments:
        customerdata = json.loads(appointments[task_id])
        car = customerdata['car']
        issue = customerdata['issue']
        price = str(customerdata['price'])
        phonenumber = customerdata['number']

        customermessage = 'Your {} needs {} at a cost of {}.\n' \
                          'Please text ok to Approve or Call'.format(car, issue, price)

        handler.createmessage(customermessage, phonenumber)

    return appointments[task_id]



@app.route('/workcomplete/<int:task_id>', methods=['GET'])
def work_complete(task_id):
    return appointments[task_id]
