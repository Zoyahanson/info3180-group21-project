from flask import Blueprint, render_template, jsonify, send_from_directory, current_app

views = Blueprint("views", __name__)

@views.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@views.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@views.route('/<file_name>.txt')
def send_text_file(file_name):
    return views.send_static_file(file_name + '.txt')


@views.after_app_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@views.app_errorhandler(404)
def page_not_found(error):
    #return render_template('404.html'), 404
    return {"error": "Route not found"}, 404
