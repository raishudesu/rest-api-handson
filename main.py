import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/create', methods=['POST'])
def create():
    try:        
        _json = request.json
        _name = _json['customer_first_name']
        _surname = _json['customer_last_name']
        _address = _json['customer_address']
        _phone = _json['mobile_number']	
        _email = _json['customer_email']
        if _name and _surname and _address and _phone and _email and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO customers (customer_first_name, customer_last_name, customer_address, mobile_number, customer_email) VALUES(%s, %s, %s, %s, %s)"
            bindData = (_name, _surname, _address, _phone, _email)            
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

@app.route('/customers/<int:id>')
def customer_details(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT customer_id, customer_first_name, customer_last_name, customer_address, customer_phone, customer_email FROM customers WHERE id =%s", id)
        customerRow = cursor.fetchone()
        respone = jsonify(customerRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/update', methods=['PUT'])
def update_customers():
    try:
        _json = request.json
        _id = _json['customer_id']
        _name = _json['customer_first_name']
        _surname = _json['customer_last_name']
        _address = _json['customer_address']
        _phone = _json['mobile_number']	
        _email = _json['customer_email']
        if _id and _name and _surname and _address and _phone and _email and request.method == 'PUT':			
            sqlQuery = "UPDATE customers SET customer_id=%s, customer_first_name=%s, customer_last_name=%s, customer_address=%s, customer_phone=%s, customer_email=%s WHERE id=%s"
            bindData = (_id, _name, _surname, _address, _phone, _email)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Family member updated successfully!')
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
def delete_customer(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM customers WHERE id =%s", (id,))
		conn.commit()
		respone = jsonify('Customer deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()