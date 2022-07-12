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
- add a favorited list
— add a downloaded list
— add an uploaded list
— only allow editing and deleting AND uploading datasets if created_by is equal to current user


ability to favorite/add datasets to profile
curate a custom dataset
'''


'''
BUGS:
datasets still shown when AWS is not connected
'''


'''
Done:

upload datasets
view datasets
'''