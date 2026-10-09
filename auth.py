from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from seguranca import exigir_login
import database as db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
    
            if 'usuario_id' in session:
                flash("Você já está autenticado")
                return redirect(url_for("leituras.index"))
            
    if request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        senha_hash = generate_password_hash(senha)
        db.criar_usuario(nome=nome, email=email, senha_hash=senha_hash)

        return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        if 'usuario_id' in session:
            flash("Você já está autenticado")
            return redirect(url_for("leituras.index"))
        
        email = request.form.get('email')
        senha_enviada = request.form.get('senha')

        db_user = db.buscar_usuario_por_email(email)
        flash(f"USUÁRIO: \n {db_user.nome}")
        if not db_user:
            flash("Usuário não encontrado")
            return redirect(url_for("auth.login"))

        if check_password_hash(db_user.senha_hash, senha_enviada):
            session["usuario_nome"] = db_user.nome
            session["usuario_id"] = db_user.id

            return redirect(url_for("leituras.index", autenticado=True))

        flash("Senha inválida")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("usuario_nome", None)
    session.pop("usuario_id", None)

    return redirect(url_for("auth.login", autenticado=False))
