
from flask import Flask, redirect
app = Flask(__name__)
@app.route('/')
@app.route('/index')
def start():
    return redirect ("/menu", code=302)
@app.route('/menu')
def menu():
    return '''
<!DOCTYPE html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>   
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <h2><a href="/lab1">Первая лабораторная</a></h2>
        <h2><a href="/lab2">Вторая лабораторная</a></h2>
        <h2><a href="/lab3">Третья лабораторная</a></h2>
        <h2><a href="/lab4">Четвёртая лабораторная</a></h2>
        <h2><a href="/lab5">Пятая лабораторная</a></h2>
        <h2><a href="/lab6">Шестая лабораторная</a></h2>
        <h2><a href="/lab7">Седьмая лабораторная</a></h2>
        <h2><a href="/lab8">Восьмая лабораторная</a></h2>
        <h2><a href="/lab9">Девятая лабораторная</a></h2>

        <footer>
            &copy; Лаптева Полина, ФБИ-24, 3 курс, 2024
        </footer>
    </body>
</html>'''

@app.route('/lab1')
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лаптева Полина Владимировна, Лабораторная 1</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: lightpurple;
                color: #333;
                line-height: 1.6;
                margin: 20px;
                font-size: 15px;
            }
            h1 {
                text-align: center;
                color: blue;
                margin-bottom: 10px;
        
        </style>
    </head>

    <body>
        <header>
            Лабораторная работа 1
        </header>

        <h1>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности. <br>        
            
            <a href="/">Меню</a>
        </h1> 
        '''
