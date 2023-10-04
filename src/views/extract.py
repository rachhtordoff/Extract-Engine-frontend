from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)
from src.utilities import jwt_util, web_scrape
from src.dependencies.openapi import DataExtractor

extract = Blueprint("extract", __name__)


@extract.route("/extract")
@jwt_util.check_jwt
def extract_data():
    return render_template(
        "pages/extract-home.html"
    )


@extract.route("/document-upload", methods=['POST'])
@jwt_util.check_jwt
def document_upload():

    post_data = request.form

    phrases_list = request.form.getlist('phrases[]')
    return jsonify(phrases_list)

    DataExtractor.extract_data_from_bank_statement(post_data)

    return render_template(
        "pages/extract-home.html"
    )


@extract.route("/url-list", methods=['POST'])
@jwt_util.check_jwt
def url_list():

    post_data = request.form
    phrases_list = request.form.getlist('phrases[]')
    url_list = post_data.get('urls', '').split("\r\n")

    scraped_websites = web_scrape.site_scrape(url_list)
    new_dict = {
        "scraped_websites": scraped_websites,
        "phrases_list": phrases_list,
        "output_typeurl": post_data.get('output_typeurl')
    }

    DataExtractor.extract_data_from_webscraped_urls(new_dict)
    return render_template(
        "pages/extract-home.html"
    )


@extract.route("/extract_pdf", methods=['POST'])
@jwt_util.check_jwt
def extract_pdf():

    post_data = request.form
    return jsonify(post_data)
    DataExtractor.extract_data_from_bank_statement(post_data)

    return render_template(
        "pages/extract-home.html"
    )
