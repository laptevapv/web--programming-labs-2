from flask import Blueprint, render_template, request, session,redirect, current_app

lab6 = Blueprint('lab6', __name__)


offices = []
for i in range(1,11):
    offices.append({'number': i, 'tenant': '', 'price':900 + i*3})


@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():
    data= request.json
    id = data['id']
    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result':offices,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
                },
                'id': id
        }
    
    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'already booked'
                        },
                        'id': id
                        }
                

                # Установить арендатора
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': f'Office {office_number} successfully booked',
                    'id': id
            }


    if data['method'] == 'cancellation':
        office_number = data['params']
        login = session.get('login')  
        if not login:
          return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                        'message': 'Office is not rented'
                    },
                    'id': id
                }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                        'message': 'You cannot cancel someone else\'s reservation'
                    },
                    'id': id
                }

            # Снятие аренды
                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': f'офис {office_number} аренда отменена',
                    'id': id
            }

        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32602,
                'message': 'Invalid office number'
        },
        'id': id
    }


    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
