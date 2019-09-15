import sys
from flask import Flask, jsonify, Blueprint
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

# sys.path.insert(0, '..')
from apiservico.servico_vaga import servicoVaga

bp_vaga = Blueprint('bp_vaga', __name__)

# curl -i http://localhost:5000/vaga
@bp_vaga.route('/vaga', methods=['GET'])
def obtem_vagas():
    resp = {'vagas': servicoVaga.obtem()}
    return jsonify(resp)

# curl -i http://localhost:5000/vaga/1
@bp_vaga.route('/vaga/<int:idVaga>', methods=['GET'])
def obtem_vaga(idVaga):
    resp = {'vaga': servicoVaga.obtem(idVaga)}
    return jsonify(resp)


@bp_vaga.route('/vaga/<int:idVaga>', methods=['DELETE'])
def remove_vaga(idVaga):
    return jsonify(servicoVaga.remove(idVaga))


# curl -i -H "Content-Type: application/json" -X POST -d '{"identificador":"A01","codigo":"B4AC41"}' http://localhost:5000/vaga
# curl -i -H "Content-Type: application/json" -X POST -d '{"identificador":"A02","codigo":"B4AC42", "estado": 3, "tipo": 2}' http://localhost:5000/vaga
# curl -i -H "Content-Type: application/json" -X POST -d '{"identificador":"A03","codigo":"B4AC43", "estado": 1, "tipo": 1, "idUsuario": 1}' http://localhost:5000/vaga
@bp_vaga.route('/vaga', methods=['POST'])
def adiciona_vaga():
    if not request.json:
        abort(404)
    
    resp = servicoVaga.adiciona(request.json)
    if 'erro' in resp:
        abort(resp['erro'], resp.get('msg'))

    return make_response(jsonify(resp), 201)