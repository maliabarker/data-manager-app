from data_app.extensions import app, db
from data_app.main.routes import main
from data_app.auth.routes import auth

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5002)

# ———MVP———

'''
TODO 

create profiles
- route & template for favorited list
— route & template for downloaded list
— route & template for uploaded list
— only allow editing and deleting if created_by is equal to current user

editing data
- edit datasets
- edit profile picture

ability to favorite/add datasets to profile
curate a custom dataset
'''


'''
BUGS:
datasets still shown when AWS is not connected
images from aws load in SO SLOW, maybe try to fix it or migrate from aws to just storing photos in folder of proj
'''


'''
Done:

upload datasets
view datasets
'''