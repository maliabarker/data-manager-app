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
# TODO create profiles
# TODO upload datasets
# TODO view datasets
# TODO search for datasets
# TODO favorite/add datasets to profile
# TODO curate a custom dataset