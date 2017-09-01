from flask import render_template,flash,redirect,session,stream_with_context,send_file,url_for,request
import requests
from app import app
from .forms import LoginForm, UploadForm
import os
import logging
from werkzeug.utils import secure_filename
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response
import parse
import writeCsv
from flask_oauthlib.client import OAuth
import json

oauth = OAuth(app)


magento = oauth.remote_app(
    'magento',
    base_url='https://www.simplewoodgoods.com/v1/',
    request_token_url='https://www.simplewoodgoods.com/oauth/token/request',
    access_token_url='https://www.simplewoodgoods.com/oauth/token/access',
    authorize_url='https://www/simplewoodgoods.com/oauth/signin',
    consumer_key=app.config['MAGENTO_KEY'],
    consumer_secret=app.config['MAGENTO_SECRET'],
    request_token_params={'scope':'listings_r'}
)



etsy = oauth.remote_app(
    'etsy',
    base_url='https://openapi.etsy.com/v2/',
    request_token_url='https://openapi.etsy.com/v2/oauth/request_token',
    access_token_url='https://openapi.etsy.com/v2/oauth/access_token',
    authorize_url='https://etsy.com/oauth/signin',
    consumer_key=app.config['ETSY_KEY'],
    consumer_secret=app.config['ETSY_SECRET'],
    request_token_params={'scope':'listings_r'}
)

services = {'etsy':etsy,
            'magento':magento}


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
            ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    data=[]
    source=[]
    if form.validate_on_submit():
        source = form.source.data
        uploaded = secure_filename(form.csvFile.data.filename)
        session['filename'] = uploaded
        session['uploadPath'] = ('./tmp/' + uploaded)
        form.csvFile.data.save(session['uploadPath'])
        if 'uploadPath' in session:
            if source == 'paypal':
                data=(parse.toList(session['uploadPath']))
                data=parse.ppClean(data)
                data=parse.ppParse(data)
                session['data']=data
            else:
                data=(parse.toList(session['uploadPath']))
                data=parse.eParse(data)
                session['data']=data
    return render_template('upload.html',
                           title = 'File Upload',
                           form=form,
                           data=data,
                           source=source
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

@app.route('/auth/<service>')
def auth(service):
    return redirect(url_for('login', service=service))

@app.route('/login/<service>', methods=['GET', 'POST'])
def login(service):
    callback = url_for(
        ('magentoauthorized'),
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return services[service].authorize(callback=callback)

@app.route('/login/authorized')

@magento.authorized_handler
def magentoauthorized(resp):
    if resp is None:
        flash(u'You need to give us access!')
        return redirect(url_for('index'))
    session['magento_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    return redirect(url_for('index'))

@etsy.authorized_handler
def etsyauthorized(resp):
    if resp is None:
        flash(u'You need to give us access!')
        return redirect(url_for('index'))
    if session.has_key('etsy_token'):
        del session['etsy_token']
    session['etsy_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    return redirect(url_for('index'))

@etsy.tokengetter
def get_etsy_token():
    return session.get('etsy_token')

@magento.tokengetter
def get_magento_token():
    return session.get('magento_token')


@app.route('/listings')
def listings():
    resp=etsy.request('https://openapi.etsy.com/v2/shops/simplewoodgoods/listings/active').data
    results=render(resp,'results')
    return render_template('listings.html',
                           title='Listings',
                           results=results
                          )

@app.route('/magento')
def magento():
    resp=magento.request('https://wwww.simplewoodgoods.com/v1/products').data
    return render_template('listings.html',
                           title='Listings',
                           results=resp
                          )

@app.route('/scopes')
def scope():
    data=etsy.request('https://openapi.etsy.com/v2/oauth/scopes').data
    data=render(data,'results')
    return render_template('scopes.html',
                           title='Scopes',
                           data=data
                          )

def render(data,key):
    data = data[key]
    return(data)
