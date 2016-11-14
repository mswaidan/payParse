from flask import render_template,flash,redirect,session,stream_with_context,send_file
from app import app
from .forms import LoginForm, UploadForm, OptionsForm
import os
import logging
from werkzeug.utils import secure_filename
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
import parse
import writeCsv

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
             { 
                 'author': {'nickname': 'John'}, 
                 'body': 'Beautiful day in Portland!' 
             },
             { 
                 'author': {'nickname': 'Susan'}, 
                 'body': 'The Avengers movie was so cool!' 
             }
            ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title = 'Sign In',
                           form=form
                          )

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        uploaded = secure_filename(form.csvFile.data.filename)
        session['filename'] = uploaded
        session['uploadPath'] = ('./tmp/' + uploaded)
        form.csvFile.data.save(session['uploadPath'])
        return redirect('/results')
    return render_template('upload.html',
                           title = 'File Upload',
                           form=form
                          )

@app.route('/results', methods=['GET', 
                                'POST'])
def results():
    form = OptionsForm()
    if 'uploadPath' in session:
        data=(parse.toList(session['uploadPath']))
        data=parse.ppClean(data)
        data=parse.ppParse(data)
        session['data']=data
        return render_template('results.html',
                               title = 'Results ',
                               filename = session['filename'],
                               form=form,
                               data=data
                              )
    else:
        return render_template('results.html',
                               title = 'Results: ',
                               filename = 'No file uploaded',
                               form=form
                              )

@app.route('/download')

def download():
    data = session['data']
    headers = Headers()
    headers.set('Content-Disposition', 'attachment',
                filename='parsed.csv')
    return Response(
                stream_with_context(writeCsv.writeCsv(data)),
                mimetype='text/csv', headers=headers
            )

#return Response(writeCsv.writeCsv(data))
#return  send_file(writeCsv.writeCsv(data),
#attachment_filename='parsed.csv',
#as_attachment=True)

