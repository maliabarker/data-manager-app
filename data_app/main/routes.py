from flask import Blueprint, request, render_template, redirect, url_for, flash, g
from flask_login import login_required
from flask_login import current_user
from datetime import date, datetime
from data_app.models import User, Dataset
from data_app.main.forms import DatasetForm, SearchForm
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
    # search_form = SearchForm()
    #
    # if search_form.validate_on_submit():
    #     return 'validated'
    # else:
    #     print(search_form.errors)

    all_datasets = Dataset.query.all()

    return render_template('search.html', datasets=all_datasets)



    # if search_form.validate_on_submit():
    #     search_query = search_form.search_param.data
    #     datasets = Dataset.query
    #     print(f'jknrewl {search_query}')
    #     datasets = datasets.filter(Dataset.title.like('%' + search_query + '%') | Dataset.description.like('%' + search_query + '%'))
    #     query = datasets.order_by(Dataset.title)
    # else:
    #     query = Dataset.query
    # pagination = paginate(query, page, error_out=False, max_per_page=6)

    # if search_form.validate_on_submit():
    #     search_query = search_form.search_param.data
    #     print(f'jknrewl {search_query}')
    #
    #     datasets = Dataset.query
    #     datasets = datasets.filter(Dataset.title.like('%' + search_query + '%') | Dataset.description.like('%' + search_query + '%'))
    #     datasets = datasets.order_by(Dataset.title).paginate(page, error_out=False, max_per_page=6)
    #
    #     print(datasets)
    #     return render_template('search.html', datasets=datasets, search_query=search_query)
    # return 'sfd'


@main.route('/index_datasets')
def index_datasets():
    all_datasets = Dataset.query.all()
    return render_template('all_datasets.html', datasets=all_datasets)

'''CREATE NEW DATASET UPLOAD TO S3 BUCKET'''
@main.route('/dataset_new', methods=['GET', 'POST'])
def dataset_new():
    form = DatasetForm()
    if form.validate_on_submit():
        image_dir = os.path.join(
            os.path.dirname(app.instance_path), 'data_app/static/img'
        )

        # check whether an input field with name 'user_file' exist
        if 'dataset_file' not in request.files:
            flash('No user_file key in request.files')
            return redirect(url_for('main.dataset_new'))

        # after confirm 'user_file' exist, get the file from input
        dataset = form.dataset_file.data
        print(dataset)

        photo = form.photo.data
        print(photo)

        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(image_dir, photo_filename))

        # check whether a file is selected
        if dataset.filename == '':
            flash('No selected file')
            return redirect(url_for('main.dataset_new'))

        # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
        if dataset and allowed_file(dataset.filename):
            output = upload_file_to_s3(dataset)

            # if upload success,will return file name of uploaded file
            if output:
                # write your code here
                # to save the file name in database
                dataset = Dataset(
                    title = form.title.data,
                    dataset_file = dataset.filename,
                    photo = photo_filename,
                    description = form.description.data
                )

                print(dataset)

                db.session.add(dataset)
                db.session.commit()
                flash("Success upload")

                return redirect(url_for('main.dataset_view', dataset_id=dataset.id))

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
@main.route('/dataset_view/<dataset_id>', methods=['GET'])
def dataset_view(dataset_id):
    dataset = Dataset.query.filter_by(id=dataset_id).one()
    df = read_csv_from_s3(dataset.dataset_file)
    # print(df.head(5))
    return render_template('view_dataset.html', dataset=dataset, dataframe=df.to_html(justify='left', show_dimensions=True, classes=['table', 'table-striped']))
