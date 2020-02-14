from flask import Flask, abort, request, jsonify
from devday import app, Swagger, Config
from devday.twiliohandler import TwilioHandler
import json

handler = TwilioHandler(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN, Config.TWILIO_NUMBER)
appointments = {}


@app.route('/sms/', methods=['GET'])
def process_sms():

    if request.headers.get('X-Twilio-Signature'):
        handler.createmessage('Hello world', to='7024154906')
    return '', 200



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
        customer['isComplete'] = False
        customer['workApproved'] = False
        customer['price'] = None
        customer['techName'] = 'Rebel Tech'
        customer['hasArrived'] = False
        customer['issue'] = 'Doesnt work'
        customer['custComment'] = 'Fix it'
        customer['techComment'] = 'Fixing your car'
        appointments[customer['id']] = json.dumps(customer)
        return json.dumps(customer)


@app.route('/getappointment/<int:task_id>', methods=['GET'])
def get_appointment(task_id):
    return appointments[task_id]


@app.route('/approveservice/<int:task_id>', methods=['GET'])
def approve_service(task_id):
    return appointments[task_id]


@app.route('/workcomplete/<int:task_id>', methods=['GET'])
def work_complete(task_id):
    return appointments[task_id]
