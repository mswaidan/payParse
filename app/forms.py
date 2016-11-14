from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Regexp

class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class UploadForm(FlaskForm):
    csvFile = FileField('The csv File')

class OptionsForm(FlaskForm):
    source = SelectField('File Source', choices=[('etsy','Etsy'),('paypal','PayPal')])
