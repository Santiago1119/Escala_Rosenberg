from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

from config import config

app=Flask(__name__)

conexion=MySQL(app)


@app.route('/patients', methods=['GET'])
def users_database():
    """Muestra los datos que estan en la tabla "patient" de la base de datos

    Returns:
        dict: retorna un json con la información de la base de datos en la tabla "patient"
    """
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT * FROM patient"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        
        for fila in datos:
            usuario = {'id_usuario': fila[0], 'nombre_usuario': fila[1], 'resultado_test': fila[2]}
            usuarios.append(usuario)
            
        return jsonify({'usuarios': usuarios})
    
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

@app.route('/patients/<id_patient>', methods=['GET'])
def search_patient(id_patient):
    """Muestra los datos de guardados de un usuario en especifico

    Returns:
        dict: retorna un json con la información del usuario en la base de datos
    """
    try:
        cursor = conexion.connection.cursor()
        sql=f"SELECT * FROM patient WHERE id_patient = '{id_patient}'"
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            usuario = {'id_usuario': datos[0], 'nombre_usuario': datos[1], 'resultado_test': datos[2]}
            return jsonify({'usuario': usuario, 'mensaje': 'Paciente encontrado'})
        else:
            return jsonify({'mensaje': 'Paciente no encontrado'})
    
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

@app.route('/patients', methods=['POST'])
def record_data():
    
    def value_question(position:int , answer: str)->int:
        """Determina que valor tiene cada pregunta

        Args:
            position int: el número de la pregunta
            answer str: Que respondio el usuario en esa pregunta

        Returns:
            int: que puntuación tuvo en esa pregunta el usuario
        """
        value_question = 0
        
        if position > 0 and position <= 5:
            if answer == 'A':
                value_question = 4
            if answer == 'B':
                value_question = 3
            if answer == 'C':
                value_question = 2
            if answer == 'D':
                value_question = 1
        
        if position > 5 and position <= 10:
            if answer == 'A':
                value_question = 1
            if answer == 'B':
                value_question = 2
            if answer == 'C':
                value_question = 3
            if answer == 'D':
                value_question = 4
        
        return value_question
            

    dictionary_return = {}
    dictionary_return['user'] = request.json['user']
    answers = request.json['answers'].copy()
    sumatory = 0
    for question in answers:
        sumatory += value_question(int(question), answers[question].upper())
    
    if sumatory >= 30 and sumatory <= 40:
        dictionary_return['resultado'] = 1
    
    if sumatory >= 26 and sumatory < 30:
        dictionary_return['resultado'] = 2
        
    if sumatory > 0 and sumatory <= 25:
        dictionary_return['resultado'] = 3
    
    try:
        cursor = conexion.connection.cursor()
        sql = f"""INSERT INTO patient (name, id_resultado) VALUES ('{dictionary_return['user']}', {dictionary_return['resultado']})"""
        cursor.execute(sql)
        conexion.connection.commit()
        
        return jsonify({'datos_ingresados': dictionary_return, 'mensaje': 'Se agregaron esos datos a la base de datos'})
    except:
        return jsonify({'mensaje': 'Error al ingresar el dato a la base de datos'})

@app.route('/patients/<id_patient>', methods=['DELETE'])
def method_name():
    pass


def page_not_found(error):
    return "<h1>La página no se encontró</h1>", 404



if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()


