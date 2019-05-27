from flask_restplus import Resource, fields

from . import swagger

ns = swagger.namespace('user', description='Auth user')

user_model = ns.model("login user model",
                        {
                            "email": fields.String(description="user email", required=True),
                            "password": fields.String(description="user password", required=True)
                        }
)

@ns.route('/login')
class Login(Resource):
    @ns.response(200, 'Success')
    @ns.response(400, 'Fail')
    @ns.expect(user_model)
    def post(self):
        return {'token': 'user token'}



