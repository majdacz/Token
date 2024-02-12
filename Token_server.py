from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'váš_tajný_klíč'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)

jwt = JWTManager(app)

uzivatele = {
    "uzivatel1": {"jmeno": "uzivatel1", "heslo": "heslo123"},
}


@app.route('/auth', methods=['POST'])
def auth():
    jmeno = request.json.get('jmeno', None)
    heslo = request.json.get('heslo', None)
    uzivatel = uzivatele.get(jmeno, None)

    if uzivatel and uzivatel['heslo'] == heslo:
        access_token = create_access_token(identity=jmeno)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Špatné jméno nebo heslo"}), 401


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Ahoj {current_user}! Máš přístup k chráněným datům."})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
