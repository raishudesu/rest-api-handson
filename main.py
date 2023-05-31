import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
from auth import require_api_key


@app.route('/create', methods=['POST'])
@require_api_key
def create():
    try:        
        _json = request.json
        _customer_first_name = _json['customer_first_name']
        _customer_last_name = _json['customer_last_name']
        _customer_address = _json['customer_address']
        _customer_phone = _json['customer_phone']	
        _customer_email = _json['customer_email']
        if _customer_first_name and _customer_last_name and _customer_address and _customer_phone and _customer_email and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO customers (customer_first_name, customer_last_name, customer_address, customer_phone, customer_email) VALUES(%s, %s, %s, %s, %s)"
            bindData = (_customer_first_name, _customer_last_name, _customer_address, _customer_phone, _customer_email)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Customer added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()  
        conn.close() 
                
     
@app.route('/customers')
@require_api_key
def customers():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT customer_id, customer_first_name, customer_last_name, customer_address, customer_phone, customer_email FROM customers")
        customerRows = cursor.fetchall()
        respone = jsonify(customerRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/customers/<int:customer_id>')
@require_api_key
def customer_details(customer_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT customer_id, customer_first_name, customer_last_name, customer_address, customer_phone, customer_email FROM customers WHERE customer_id =%s", customer_id)
        customerRow = cursor.fetchone()
        if customerRow is None:
            response = jsonify({'error': 'No existing customer with the specified id'})
            response.status_code = 404
        else:
            response = jsonify(customerRow)
            response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/update', methods=['PUT'])
@require_api_key
def update_customers():
    try:
        _json = request.json
        _customer_id = _json['customer_id']
        _customer_first_name = _json['customer_first_name']
        _customer_last_name = _json['customer_last_name']
        _customer_address = _json['customer_address']
        _customer_phone = _json['customer_phone']	
        _customer_email = _json['customer_email']
        if _customer_id and _customer_first_name and _customer_last_name and _customer_address and _customer_phone and _customer_email and request.method == 'PUT':			
            sqlQuery = "UPDATE customers SET customer_first_name=%s, customer_last_name=%s, customer_address=%s, customer_phone=%s, customer_email=%s WHERE customer_id=%s"
            bindData = (_customer_first_name, _customer_last_name, _customer_address, _customer_phone, _customer_email, _customer_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Customer updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/delete/<int:id>', methods=['DELETE'])
@require_api_key
def delete_customer(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id FROM customers WHERE customer_id =%s", (id,))
        customer_id = cursor.fetchone()

        if customer_id is None:
            response = jsonify({'error': 'No existing customer with the specified id'})
            response.status_code = 404
        else:
            cursor.execute("DELETE FROM customers WHERE customer_id =%s", (id,))
            conn.commit()
            response = jsonify('Customer deleted successfully!')
            response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()     
                
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record does not exist: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()