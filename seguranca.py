from flask import flash, redirect, session, url_for


def exigir_login():
    # Complete esta função durante a avaliação.
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))
    
    # Ela deve verificar se existe session["usuario_id"].
    # Caso não exista, redirecione para auth.login.
    return None
