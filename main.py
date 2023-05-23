import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/create', methods=['POST'])
def create():
    try:        
        _json = request.json
        _name = _json['name']
        _mddl_ntl = _json['mddl_ntl']
        _surname = _json['surname']
        _mobile_number = _json['mobile_number']	
        if _name and _mddl_ntl and _surname and _mobile_number and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO family_details (name, mddl_ntl, surname, mobile_number) VALUES(%s, %s, %s, %s)"
            bindData = (_name, _mddl_ntl, _surname, _mobile_number)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Family member added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()  
        conn.close() 
                
     
@app.route('/family_details')
def family_details():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, mddl_ntl, surname, mobile_number FROM family_details")
        family_detailsRows = cursor.fetchall()
        respone = jsonify(family_detailsRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/family_details/<int:id>')
def table_details(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(f"SELECT id, name, mddl_ntl, surname, mobile_number FROM family_details WHERE id ={id}")
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/update', methods=['PUT'])
def update_family_details():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _mddl_ntl = _json['mddl_ntl']
        _surname = _json['surname']
        _mobile_number = _json['mobile_number']	
        if _name and _mddl_ntl and _surname and _mobile_number and _id and request.method == 'PUT':			
            sqlQuery = "UPDATE family_details SET name=%s, mddl_ntl=%s, surname=%s, mobile_number=%s WHERE id=%s"
            bindData = (_name, _mddl_ntl, _surname, _mobile_number, _id)
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
def delete_bacaltos_family(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM family_details WHERE id =%s", (id,))
		conn.commit()
		respone = jsonify('Family member deleted successfully!')
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