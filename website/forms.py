from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import email_validator

class Registrar(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=15)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    enviar = SubmitField('Enviar')

class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=15)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    enviar = SubmitField('Enviar')