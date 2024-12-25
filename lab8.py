from flask import Blueprint, render_template, request, session,redirect, current_app, flash, url_for
from db import db
from db.models import users,articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_
lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    user_login = session.get('login', "anonymous")  # По умолчанию "anonymous"
    return render_template('lab8/lab8.html', login=session.get('login'))

@lab8.route('/lab8/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error = 'Такой пользователь уже существует')
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    session['login'] = login_form
    return redirect('/lab8/')

@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
            return render_template('lab8/login.html')
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    user = users.query.filter_by(login = login_form).first()
    if user:
         if check_password_hash(user.password, password_form):
              login_user(user)
              session['login'] = user.login
              return redirect ('/lab8/')
    
    return render_template('/lab8/login.html', error = 'Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/articles', methods=['GET'])
@login_required
def articles_list():
    # Получаем все статьи текущего пользователя
    all_articles = articles.query.filter_by(user_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=all_articles)


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    session.pop('login', None) 
    return redirect('/lab8/')


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    # Получаем данные из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on' 
    is_favorite = request.form.get('is_favorite') == 'on'  

    if not title or not article_text:
        return render_template('lab8/create.html', error="Название и текст статьи обязательны.")

    # Создаём новую статью
    new_article = articles(
        user_id=current_user.id,
        title=title,
        article_text=article_text,
        is_public=is_public,
        is_favorite=is_favorite,
    )

    # Сохраняем статью в базе данных
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles')


@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.user_id != current_user.id:
        return redirect('/lab8/articles')

    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)

    # Получаем данные из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'  
    is_favorite = request.form.get('is_favorite') == 'on'  

    if not title or not article_text:
        return render_template('lab8/edit.html', article=article, error="Название и текст статьи обязательны.")

    # Обновляем статью
    article.title = title
    article.article_text = article_text
    article.is_public = is_public
    article.is_favorite = is_favorite
    db.session.commit()

    return redirect('/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    # Получаем статью по ID
    article = articles.query.get_or_404(article_id)

    if article.user_id != current_user.id:
        return redirect ('/lab8')

    db.session.delete(article)
    db.session.commit()

    flash("Статья успешно удалена!", "success")
    return redirect ('/lab8/articles')


@lab8.route('/lab8/public_articles', methods=['GET'])
def public_articles():
    # Получаем все статьи, которые являются публичными
    public_articles = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/public_articles.html', articles=public_articles)

@lab8.route('/lab8/search', methods=['GET', 'POST'])
@login_required
def search_articles():
    query = request.args.get('query', '').strip()  
    results = []

    if query:
        results = articles.query.filter(
            or_(
                articles.title.ilike(f"%{query}%"),  
                articles.article_text.ilike(f"%{query}%")  
            ),
            articles.user_id == current_user.id  
        ).all()
    else:
        # Если нет запроса, выводим все статьи пользователя
        results = articles.query.filter_by(user_id=current_user.id).all()

    return render_template('lab8/articles.html', articles=results, query=query)