#!/usr/bin/env python3
"""
Compiler Playground — Lance avec : python start.py
Puis ouvre http://localhost:5050
"""
import sys, os, threading, webbrowser, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS
except ImportError:
    print("\n[!] Flask non installe. Lance :\n    pip install flask flask-cors\n")
    sys.exit(1)

from lexical_analyser import tokenize
from parser import Parser, Decl, Assign, BinOp, Num, Id, Str
from semantic_analyzer import SemanticAnalyzer, SemanticError

BASE = os.path.dirname(os.path.abspath(__file__))
app  = Flask(__name__, static_folder=BASE)
CORS(app)

# symbol table persistante entre les requetes
_symbol_table = {}

# ── serialisation Token (pas de to_dict dans l'original) ───────
def tok_to_dict(t):
    return {'type': t.type, 'value': t.value}

# ── serialisation AST (pas de to_dict dans l'original) ─────────
def node_to_dict(node):
    if isinstance(node, Decl):
        return {'kind': 'Decl', 'type': node.type, 'name': node.name}
    if isinstance(node, Assign):
        return {'kind': 'Assign', 'name': node.name, 'expr': node_to_dict(node.expr)}
    if isinstance(node, BinOp):
        return {'kind': 'BinOp', 'op': node.op,
                'left': node_to_dict(node.left), 'right': node_to_dict(node.right)}
    if isinstance(node, Num):
        return {'kind': 'Num', 'value': node.value}
    if isinstance(node, Id):
        return {'kind': 'Id', 'name': node.name}
    if isinstance(node, Str):
        return {'kind': 'Str', 'value': node.value}
    return {}

# ── routes ──────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(BASE, 'index.html')

@app.route('/api/run', methods=['POST'])
def run():
    global _symbol_table
    data   = request.get_json(force=True)
    source = data.get('source', '').strip()
    if not source:
        return jsonify({'error': 'Empty source'}), 400

    result = {'source': source, 'stages': {}}

    # Stage 1 – Lexer
    try:
        tokens = tokenize(source)
        result['stages']['lexer'] = {
            'ok': True,
            'tokens': [tok_to_dict(t) for t in tokens]
        }
    except SyntaxError as e:
        result['stages']['lexer'] = {'ok': False, 'error': str(e)}
        result['failed_at'] = 'lexer'
        return jsonify(result)

    # Stage 2 – Parser
    try:
        ast = Parser(tokens).stmt()
        result['stages']['parser'] = {
            'ok': True,
            'ast': node_to_dict(ast),
            'repr': repr(ast)
        }
    except SyntaxError as e:
        result['stages']['parser'] = {'ok': False, 'error': str(e)}
        result['failed_at'] = 'parser'
        return jsonify(result)

    # Stage 3 – Semantic
    # On cree l'analyzeur puis on injecte la symbol table de session directement
    try:
        analyzer = SemanticAnalyzer()
        analyzer.symbol_table._table = dict(_symbol_table)
        inferred      = analyzer.analyze(ast)
        _symbol_table = dict(analyzer.symbol_table._table)
        result['stages']['semantic'] = {
            'ok': True,
            'type': inferred,
            'symbol_table': _symbol_table
        }
    except SemanticError as e:
        result['stages']['semantic'] = {
            'ok': False,
            'error': str(e),
            'symbol_table': dict(_symbol_table)
        }
        result['failed_at'] = 'semantic'
        return jsonify(result)

    result['symbol_table'] = _symbol_table
    return jsonify(result)

@app.route('/api/reset', methods=['POST'])
def reset():
    global _symbol_table
    _symbol_table = {}
    return jsonify({'ok': True, 'symbol_table': {}})

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({'ok': True, 'symbol_table': _symbol_table})

# ── main ────────────────────────────────────────────────────────
if __name__ == '__main__':
    PORT = 5050
    URL  = f'http://localhost:{PORT}'
    print("============================================")
    print("       Compiler Playground")
    print("============================================")
    print(f"  URL  ->  {URL}")
    print("  Stop ->  Ctrl+C")
    print("============================================\n")
    def open_browser():
        time.sleep(1.2)
        webbrowser.open(URL)
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)