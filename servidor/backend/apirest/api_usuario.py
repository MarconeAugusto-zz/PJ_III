import sys
from flask import Flask, jsonify, Blueprint
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from apirest.utils.auth import generate_token, verify_token, requires_auth_user, requires_auth_admin

# sys.path.insert(0, '..')
from apiservico.servico_usuario import servicoUsuario

bp_usuario = Blueprint('bp_usuario', __name__)

# curl -i http://localhost:5000/usuario
@bp_usuario.route('/usuario', methods=['GET'])
def obtem_usuarios():
    resp = {'usuarios': servicoUsuario.obtem()}
    return jsonify(resp)

# curl -i http://localhost:5000/usuario/1
@bp_usuario.route('/usuario/<int:idUsuario>', methods=['GET'])
def obtem_usuario(idUsuario):
    resp = {'usuario': servicoUsuario.obtem(idUsuario)}
    return jsonify(resp)

# curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/usuario/<ID>
@bp_usuario.route('/usuario/<int:idUsuario>', methods=['DELETE'])
def remove_usuario(idUsuario):
    resp = servicoUsuario.removeUsuario(idUsuario)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))

    return make_response(jsonify(resp), 201)


# curl -i -H "Content-Type: application/json" -X POST -d '{"identificadorVaga": "A01", "novoEstado": 1}' http://localhost:5000/usuario
# curl -i -H "Content-Type: application/json" -X POST -d '{"nome":"Joao","sobrenome":"Silva","email":"joao","senha":"1234","tipo":2}' http://localhost:5000/usuario
# curl -i -H "Content-Type: application/json" -X POST -d '{"nome":"Vinicius","sobrenome":"Souza","email":"vini","senha":"1234"}' http://localhost:5000/usuario
# curl -i -H "Content-Type: application/json" -X POST -d '{"nome":"Vinicius","sobrenome":"Souza","email":"vini","senha":"1234","tipo":1}' http://localhost:5000/usuario
@bp_usuario.route('/usuario', methods=['POST'])
def adiciona_usuario():
    if not request.json:
        abort(404)
    
    resp = servicoUsuario.adiciona(request.json)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))

    return make_response(jsonify(resp), 201)

# curl -i http://localhost:5000/usuario/1/vagas
@bp_usuario.route('/usuario/<int:idUsuario>/vagas', methods=['GET'])
def obtem_vagas(idUsuario):
    resp = servicoUsuario.obtemVagas(idUsuario)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))
    return jsonify(resp)


# curl -i http://localhost:5000/usuarios/vagas
@bp_usuario.route('/usuarios/vagas', methods=['GET'])
def obtem_usuarios_vagas():
    resp = {'usuarios': servicoUsuario.obtem(comVagas=True)}
    return jsonify(resp)

# curl -i -H "Content-Type: application/json" -X POST -d '{"email":"pedro@email.com.br", "senha": "1234"}' http://localhost:5000/usuario/login
# curl -i -H "Content-Type: application/json" -X POST -d '{"email":"vini@email.com.br", "senha": "1234"}' http://localhost:5000/usuario/login
@bp_usuario.route("/usuario/login", methods=["POST"])
def create_token():
    if not request.json:
        abort(404)

    usuario = servicoUsuario.checkLogin(request.json)
    if 'erro' in usuario:
        abort(usuario['erro'], usuario.get('msg'))

    return jsonify(token=generate_token(usuario))


@bp_usuario.route("/usuario/check_token", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403

# curl -i -H "Authorization: eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MDIwNTE1OCwiZXhwIjoxNTcxNDE0NzU4fQ.eyJpZCI6MiwiZW1haWwiOiJwZWRyb0BlbWFpbC5jb20uYnIiLCJ0aXBvIjoyfQ.GiWRFBXNgBE4Y6GQRneTtvzcRi8yectSE07TapXLyXHivRt8kOsEUP57XWwjx6u2RlTOBQi7VmSBb7UrUY0mEQ" http://localhost:5000/usuario/teste_auth_user
@bp_usuario.route("/usuario/teste_auth_user", methods=["GET"])
@requires_auth_user
def teste_auth_user():
    return jsonify({'resp': 'muito bem, autenticado como user'})

# curl -i -H "Authorization: eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MDIwNTE1OCwiZXhwIjoxNTcxNDE0NzU4fQ.eyJpZCI6MiwiZW1haWwiOiJwZWRyb0BlbWFpbC5jb20uYnIiLCJ0aXBvIjoyfQ.GiWRFBXNgBE4Y6GQRneTtvzcRi8yectSE07TapXLyXHivRt8kOsEUP57XWwjx6u2RlTOBQi7VmSBb7UrUY0mEQ" http://localhost:5000/usuario/teste_auth_admin
@bp_usuario.route("/usuario/teste_auth_admin", methods=["GET"])
@requires_auth_admin
def teste_auth_admin():
    return jsonify({'resp': 'muito bem, autenticado como admin'})