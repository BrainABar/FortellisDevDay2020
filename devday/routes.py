from flask import Flask, abort, request, jsonify, render_template
from devday import app, Swagger, Config
from devday.twiliohandler import TwilioHandler
import json

handler = TwilioHandler(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN, Config.TWILIO_NUMBER)
appointments = {}


@app.route('/sms/', methods=['POST'])
def process_sms():

    if request.headers.get('X-Twilio-Signature'):
        body = request.form['Body']
        fromnumber = request.form['From']

        for customer in appointments.values():
            if customer['number'] in fromnumber:
                if 'ok' in body.lower():
                    customer['workApproved'] = True
                    appointments[customer['id']] = customer
                    customermessage = 'Thank you {}. We shall notify you once work is complete'.format(customer['name'])
                    handler.createmessage(body=customermessage, to=fromnumber)
                    return '<Response></Response>'

        customermessage = 'You do not have an appointment with Rebel Shop. Call to set one up.'
        handler.createmessage(body=customermessage, to=fromnumber)

    return 'Hello'


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
        appointments[customer['id']] = customer

        customermessage = '{}, you have an appointment at Rebel Shop at {}, for your {}'.format(name, time, customer['car'])

        handler.createmessage(customermessage, to=customer['number'])

        return json.dumps(customer)


@app.route('/getappointment/<int:task_id>', methods=['POST'])
def get_appointment(task_id):

    if task_id in appointments:
        customer = appointments[task_id]
        customer['hasArrived'] = True
        appointments[customer['id']] = customer

        car = customer['car']
        phonenumber = customer['number']
        customermessage = 'Welcome to the Rebel Shop Tracking.' \
                          'You will receive updates regarding your {}'.format(car)
        handler.createmessage(customermessage, phonenumber)

        return json.dumps(appointments[customer['id']])

    return 'Does not exist'


@app.route('/approveservice/<int:task_id>', methods=['POST'])
def approve_service(task_id):

    if task_id in appointments:
        customer = appointments[task_id]
        car = customer['car']
        issue = customer['issue']
        price = str(customer['price'])
        phonenumber = customer['number']
        customermessage = 'Your {} needs {} at a cost of {}.\n' \
                          'Please text ok to Approve or Call 555-555-5555'.format(car, issue, price)
        handler.createmessage(customermessage, phonenumber)

    return json.dumps(appointments[task_id])


@app.route('/workcomplete/<int:task_id>', methods=['POST'])
def work_complete(task_id):

    if task_id in appointments:
        customer = appointments[task_id]
        customer['isComplete'] = True
        appointments[customer['id']] = customer

        name = customer['name']
        car = customer['car']
        client_id = customer['id']
        phonenumber = customer['number']
        custommessage = 'Hello {}, you {} work is complete and ready for pick up\n' \
                        'billing statement at: rebelshop.domain/{}{}'.format(name, car, client_id, '12345')
        handler.createmessage(custommessage, phonenumber)

        return json.dumps(customer)

