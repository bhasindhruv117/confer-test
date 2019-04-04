from flask_restful import Api
from flask_jwt_extended import JWTManager
import api.models as models
import api.resources as resources
from api.models import db, app
api = Api(app)
@app.before_first_request
def create_tables():
    db.create_all()

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti=jti)

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.AuthGenerator,'/authgen')
api.add_resource(resources.QRGenerator,'/qrgen')
api.add_resource(resources.PublicDiscussion,'/discussion')

import api.views
