from flask import Flask, abort, request, jsonify
from flasgger import Swagger
import json


app = Flask(__name__)
Swagger(app)

appointments = {}


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


@app.route('/workcomplete/<int:task_id>', method=['GET'])
def work_complete(task_id):
    return appointments[task_id]


if __name__ == '__main__':
    app.run()
