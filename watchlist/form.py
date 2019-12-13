'''
@Author: your name
@Date: 2019-12-11 14:08:00
@LastEditTime: 2019-12-11 14:08:20
@LastEditors: Please set LastEditors
@Description: In User Settings Edit      
@FilePath: \watchlist\watchlist\Form.py
'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class HelloForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('Message', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()