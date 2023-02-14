from .extensions import db

class Score_table_rosenberg(db.Model):
    id_resultado = db.Column(db.Integer, primary_key=True)
    resultado = db.Column(db.String(100))
    patients = db.relationship('Patient', back_populates='resultado')

class Patient(db.Model):
    id_patient = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    id_resultado = db.Column(db.ForeignKey('resultado.id_resultado'))
    resultado = db.relationship('Score_table_rosenberg', back_populates='pacientes')