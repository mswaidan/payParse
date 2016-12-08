from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Regexp

class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class UploadForm(FlaskForm):
    csvFile = FileField('File',validators=[
            FileRequired(),
            FileAllowed(['csv'], '.csv')
        ])
    source = SelectField('Source',
                         choices=[('paypal','PayPal'),('etsy','Etsy')]
                        )
