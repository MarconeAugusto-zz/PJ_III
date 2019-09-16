import sys
from flask import Flask, jsonify, Blueprint
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

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


@bp_usuario.route('/usuario/<int:idUsuario>', methods=['DELETE'])
def remove_usuario(idUsuario):
    return jsonify(servicoUsuario.remove(idUsuario))


# curl -i -H "Content-Type: application/json" -X POST -d '{"nome":"Joao","sobrenome":"Silva","login":"joao","senha":"1234","tipo":2}' http://localhost:5000/usuario
# curl -i -H "Content-Type: application/json" -X POST -d '{"nome":"Vinicius","sobrenome":"Souza","login":"vini","senha":"1234"}' http://localhost:5000/usuario
# curl -i -H "Content-Type: application/json" -X POST -d '{"nome":"Vinicius","sobrenome":"Souza","login":"vini","senha":"1234","tipo":1}' http://localhost:5000/usuario
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