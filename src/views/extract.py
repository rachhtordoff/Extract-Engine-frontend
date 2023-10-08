from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    jsonify
)
from src.utilities import jwt_util
from src.dependencies import sqs
from src.dependencies.users_api import UserApi
from src import config
import os

extract = Blueprint("extract", __name__)


@extract.route("/extract")
@jwt_util.check_jwt
def extract_data():
    return render_template(
        "pages/extract-home.html",
        session=session['info-message']
    )


@extract.route("/documents")
@jwt_util.check_jwt
def documents():
    session['info-message'] = ''

    get_doc_names_list = UserApi().get_documents(session['id'])

    get_document_urls = UserApi().get_document_urls(session['id'], get_doc_names_list)

    return render_template(
        "pages/document-home.html",
        session=session['info-message'],
        get_document_urls=get_document_urls.get('urls', {})
    )


@extract.route("/document-upload", methods=['POST'])
@jwt_util.check_jwt
def document_upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        file_content = file.read()
        if len(file_content) < config.MAX_FILE_SIZE:
            file_name =os.path.splitext(file.filename)[0]
        else:
            session['info-message'] = 'file-too-large'
            return redirect('./extract')
    else:
        if not file:
            session['info-message'] = 'no-file-selected'
            return redirect('./extract')

        if not allowed_file(file.filename):
            session['info-message'] = 'not-allowed-file'
            return redirect('./extract')

    post_data = request.form

    phrases_list = request.form.getlist('phrases[]')

    new_extract = {
        "user_id": session['id'],
        "file_Type": post_data.get('output_typeurl'),
        "extraction_type": 'urls'
    }
    
    get_extract_data =  UserApi().new_extract(new_extract)
    new_doc_upload =  UserApi().post_document(get_extract_data[0]['id'], file_name, file_content)

    create_doc = {
        "phrases_list": phrases_list,
        "output_typeurl": post_data.get('output_typeurl'),
        "type": 'file',
        'filename': file_name,
        "id": get_extract_data[0]['id'],
        "access_token": session['access_token']
    }

    sqs.send_create_doc_data(create_doc)

    session['info-message'] = 'document-creating'
    return redirect('./extract')

@extract.route("/url-list", methods=['POST'])
@jwt_util.check_jwt
def url_list():
    post_data = request.form
    phrases_list = request.form.getlist('phrases[]')
    url_list = post_data.get('urls', '').split("\r\n")

    new_extract = {
        "user_id": session['id'],
        "file_Type": post_data.get('output_typeurl'),
        "extraction_type": 'urls'
    }

    get_extract_data =  UserApi().new_extract(new_extract)

    create_doc = {
        "url_list": url_list,
        "phrases_list": phrases_list,
        "output_typeurl": post_data.get('output_typeurl'),
        "type": 'urls',
        "id": get_extract_data[0]['id'],
        "access_token": session['access_token']
    }

    sqs.send_create_doc_data(create_doc)

    session['info-message'] = 'document-creating'
    return redirect('./extract')



@extract.route("/extract_pdf", methods=['POST'])
@jwt_util.check_jwt
def extract_pdf():

    post_data = request.form
    return jsonify(post_data)

    return redirect('./extract')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS
