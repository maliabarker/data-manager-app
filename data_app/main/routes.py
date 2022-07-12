from distutils.command.upload import upload
from flask import Blueprint, request, render_template, redirect, url_for, flash, g, jsonify
from flask_login import login_required
from flask_login import current_user
from datetime import date, datetime
from data_app.models import User, Dataset
from data_app.main.forms import DatasetForm, SearchForm
from flask_paginate import Pagination, get_page_parameter
import os

from werkzeug.utils import secure_filename
from data_app.util.helpers import upload_file_to_s3, read_csv_from_s3

from data_app.extensions import app, db, bcrypt

# for uploading files
ALLOWED_EXTENSIONS = {'png', 'csv'}

main = Blueprint("main", __name__)

# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.before_app_request
def before_request():
    g.search_form = SearchForm()

@main.route('/')
def homepage():
    return render_template('home.html', user=current_user)

@main.route('/search/<int:page>', methods=['GET', 'POST'])
def search(page=1):
    search_query = request.args.get('search_param')

    page = request.args.get(get_page_parameter(), type=int, default=1)

    datasets = Dataset.query.filter(
        Dataset.title.like(f'%{search_query}%') | Dataset.description.like(f'%{search_query}%'))
    datasets = datasets.order_by(Dataset.title)  # override datasets

    pagination = Pagination(page=page, total=datasets.count(), record_name='datasets')

    return render_template('search.html', search_query=search_query, datasets=datasets, pagination=pagination)

@main.route('/datasets')
def index_datasets():
    all_datasets = Dataset.query.all()
    return render_template('all_datasets.html', datasets=all_datasets)

'''CREATE NEW DATASET UPLOAD TO S3 BUCKET'''
@main.route('/datasets/new', methods=['GET', 'POST'])
@login_required
def dataset_new():
    form = DatasetForm()
    if form.validate_on_submit():
        # image_dir = os.path.join(
        #     os.path.dirname(app.instance_path), 'data_app/static/img'
        # )

        # check whether an input field with name 'user_file' exist
        if 'dataset_file' not in request.files or 'photo' not in request.files:
            flash('No dataset_file key or photo_file key in request.files')
            return redirect(url_for('main.dataset_new'))
        

        # after confirm 'user_file' exist, get the file from input
        dataset = form.dataset_file.data
        photo = form.photo.data
        print(dataset)
        print(photo)
        
        # photo_filename = secure_filename(photo.filename)
        # photo.save(os.path.join(image_dir, photo_filename))

        # check whether a file is selected
        if dataset.filename == '' or photo.filename == '':
            flash('No selected file for dataset or photo')
            return redirect(url_for('main.dataset_new'))

        # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
        if dataset and allowed_file(dataset.filename) and photo and allowed_file(photo.filename):
            output1 = upload_file_to_s3(dataset, 'datasets')
            output2 = upload_file_to_s3(photo, 'dataset_pics')

            # if upload success,will return file name of uploaded file
            if output1 and output2:
                # write your code here
                # to save the file name in database
                dataset = Dataset(
                    title = form.title.data,
                    dataset_file = dataset.filename,
                    photo = photo.filename,
                    description = form.description.data,
                    download_count = 0,
                    created_by = current_user
                )

                print(dataset)
                dataset = db.session.merge(dataset)

                db.session.add(dataset)
                db.session.commit()
                flash("Success upload")

                return redirect(url_for('main.dataset', dataset_id=dataset.id))

            # upload failed, redirect to upload page
            else:
                flash("Unable to upload, try again")
                return redirect(url_for('main.dataset_new'))

        # if file extension not allowed
        else:
            flash("File type not accepted,please try again.")
            return redirect(url_for('main.dataset_new'))

    return render_template('new_dataset.html', form=form)


'''VIEW ONE DATASET'''
@main.route('/datasets/<dataset_id>', methods=['GET'])
def dataset(dataset_id):
    dataset = Dataset.query.filter_by(id=dataset_id).one()
    df = read_csv_from_s3(dataset.dataset_file)
    # print(df.head(5))
    return render_template('view_dataset.html', dataset=dataset, dataframe=df.to_html(justify='left', show_dimensions=True, classes=['table', 'table-striped']))

@main.route('/datasets/<dataset_id>/download', methods=['GET'])
def download_file(dataset_id):
    # TODO: add dataset to user downloaded files
    dataset = db.session.query(Dataset).filter_by(id=dataset_id).one()
    dataset.download_count += 1

    db.session.add(dataset)
    db.session.commit()

    return jsonify({'fileUrl': f'https://datamanagementapp.s3.us-west-1.amazonaws.com/{dataset.dataset_file}'})

@main.route('/datasets/<dataset_id>/delete', methods=['POST'])
def delete_file(dataset_id):
    db.session.query(Dataset).filter_by(id=dataset_id).delete()
    db.session.commit()

    return redirect(url_for('main.index_datasets'))

'''VIEW PROFILE'''
@main.route('/profile/<username>', methods=['GET'])
def view_profile(username):
    this_user = User.query.filter_by(username=username).one()
    uploaded_dfs = Dataset.query.filter_by(created_by_id=this_user.id).all()
    # print(this_user.downloaded_datasets)
    print(uploaded_dfs)
    return render_template('profile.html', user=this_user, uploaded_datasets=uploaded_dfs)