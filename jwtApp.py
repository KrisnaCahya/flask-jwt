from multiprocessing.dummy import current_process
from flask import Flask, jsonify, make_response, request, render_template
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager # mengimport library

app = Flask(__name__, static_url_path='/static') #menuju url static

#membuat akun
account = {
  "username": "test",
  "password": "test"
}

#setup the flask-jwt-extended
app.config["JWT_SECRET_KEY"] = "myjwtsecretkey" #mengatur untuk screet key
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"] # tempat program akan mengakses jwt 
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    # IF USERNAME OR PASSWORD IS WRONG
    if username != account["username"] or password != account["password"]:
      return jsonify({"message": "bad username or password"}),401
    
    # IF USERNAME AND PASSWORD IS RIGHT
    access_token = create_access_token(identity=account) #mengenerate akses token
    response = make_response(jsonify(access_token=access_token), 200) # membuat respon dengan isi token
    response.set_cookie('access_token_cookie', access_token) #mengirim cookie ke client dengan isi token yang sudah di buat
    return response

# JWT PROTECTED ROUTE
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # GET JWT IDENTITY
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user),200

@app.route("/", methods=["GET"])
def mainPage():
    return 200

if(__name__ == "__main__"):
  app.run(port=5000)