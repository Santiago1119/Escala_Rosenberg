from flask import Flask, jsonify, request, json
from flask_mysqldb import MySQL

from config import config

app=Flask(__name__)

conexion=MySQL(app)


@app.route('/patients', methods=['GET'])
def users_database()->dict:
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
def search_patient(id_patient:int)->dict:
    """Muestra los datos de guardados en la base de datos de un usuario en especifico

    Args:
        id_patient (int): id del paciente que se busca en la base de datos

    Returns:
        dict: retorna un json que contiene la información almacenada en la base de datos
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
def insert_data()->dict:
    """inserta en la base de datos en nombre del usuario y el resultado del test

    Returns:
        dict: returna un json con la información que se insertó en la base de datos
    """
    def value_question(position:int , answer: str)->int:
        """Determina que valor tiene cada pregunta

        Args:
            position: int: el número de la pregunta
            answer: str: Que opción respondio el usuario en esa pregunta

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
    dictionary_return ['user']= request.json['user']
    answers = request.json['answers'].copy()
    sumatory = 0
    
    for answer in answers:
        sumatory += value_question(int(answer), answers[answer].upper())
    
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
def delete_patient(id_patient:int)->dict:
    """Elimina un usuario de la base de datos

    Args:
        id_patient (int): id del usuario de la base de datos que se desea eliminar

    Returns:
        dict: un json con el id del paciente que se eliminó de la base de datos
    """
    
    patient = search_patient(id_patient)
    patient_dict = json.loads(patient.get_data())
    
    try:
        cursor = conexion.connection.cursor()
        sql = f"DELETE FROM patient WHERE id_patient = {id_patient}"
        cursor.execute(sql)
        conexion.connection.commit()
        
        return jsonify({'información del paciente eliminado': patient_dict['usuario']})
    except:
        return jsonify({'mensaje': 'Error al eliminar al paciente de la base de datos'})

@app.route('/patients/<id_patient>', methods=['PUT'])
def update_patient(id_patient:int)->dict:
    """Actualiza un registro en la base de datos, y en un json debe recibir la información nueva que tendra ese paciente

    Args:
        id_patient (int): id del usuario de la base de datos que se desea actualizar

    Returns:
        dict: un json con la información que se actualizará de la base de datos, la nueva información y el id del paciente
    """
    patient = search_patient(id_patient)
    patient_dict = json.loads(patient.get_data())
    
    try:
        result = int(request.json['result'])
        name = request.json['name']
        
        cursor = conexion.connection.cursor()
        sql = f"""UPDATE patient SET name = '{name}', id_resultado = {result} 
                WHERE id_patient = {id_patient}"""
        cursor.execute(sql)
        conexion.connection.commit()
        
        return jsonify({'información que se actualizo': patient_dict['usuario'],
                        'id paciente': id_patient,
                        'nueva información': request.json})
    except:
        return jsonify({'mensaje': 'Error al actualizar la base de datos'})

def page_not_found(error:int)->str:
    """Si la página de la URL no existe envia un mensaje advirtiendo

    Args:
        error (int): error de petición HTTP

    Returns:
        str: etiqueta HTML que dice que la página no se encontró
    """
    return "<h1>La página no se encontró</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()


