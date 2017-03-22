import logging

from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def splash_page():
    return render_template('splash_page.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/test/<row>')
def test(row):
    return 'Hello World %s' % row

@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']  
    return render_template('submitted_form.html', name=name, email=email, site=site, comments=comments)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)    