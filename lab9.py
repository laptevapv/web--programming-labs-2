from flask import Blueprint, render_template,request, redirect, url_for,session

lab9 = Blueprint('lab9', __name__)


@lab9.route('/lab9', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name  # Сохраняем имя в сессии
        return redirect(url_for('lab9.age', name=name))
    return render_template('lab9/index.html')

# Шаг 2: Ввод возраста
@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    name = request.args.get('name')
    if request.method == 'POST':
        age = int(request.form['age'])
        session['age'] = age 
        return redirect(url_for('lab9.gender', name=name, age=age))
    return render_template('lab9/age.html', name=name)

# Шаг 3: Ввод пола
@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form['gender']
        session['gender'] = gender
        return redirect(url_for('lab9.preference1', name=name, age=age, gender=gender))
    return render_template('lab9/gender.html', name=name, age=age)

# Шаг 4: Первый выбор предпочтений
@lab9.route('/lab9/preference1', methods=['GET', 'POST'])
def preference1():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    if request.method == 'POST':
        preference1 = request.form['preference1']
        session['preference1'] = preference1
        return redirect(url_for('lab9.preference2', name=name, age=age, gender=gender, preference1=preference1))
    return render_template('lab9/preference1.html', name=name, age=age, gender=gender)

# Шаг 5: Второй выбор предпочтений
@lab9.route('/lab9/preference2', methods=['GET', 'POST'])
def preference2():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    preference1 = request.args.get('preference1')
    if request.method == 'POST':
        preference2 = request.form['preference2']
        session['preference2'] = preference2
        return redirect(url_for('lab9.final', name=name, age=age, gender=gender, preference1=preference1, preference2=preference2))
    return render_template('lab9/preference2.html', name=name, age=age, gender=gender, preference1=preference1)

# Шаг 6: Финальное поздравление
@lab9.route('/lab9/final', methods=['GET'])
def final():
    try:
        # Получение параметров
        name = request.args.get('name')
        age = request.args.get('age')
        gender = request.args.get('gender')
        preference1 = request.args.get('preference1')
        preference2 = request.args.get('preference2')

        # Проверка обязательных параметров
        if not all([name, age, gender, preference1, preference2]):
            return "Некорректный запрос: не все параметры переданы", 400

        age = int(age)  # Преобразование возраста в число

        # Логика поздравления
        if age < 18:
            if gender == 'male':
                message = f"Поздравляю тебя, {name}! Желаю, чтобы ты быстро вырос, был умным, смелым и сильным!"
            else:
                message = f"Поздравляю тебя, {name}! Желаю, чтобы ты быстро выросла, была умной, доброй и красивой!"
        else:
            if gender == 'male':
                message = f"Поздравляю вас, {name}! Желаю успехов в работе, здоровья и радости!"
            else:
                message = f"Поздравляю вас, {name}! Желаю счастья, красоты и вдохновения!"

        # Логика выбора изображения
        if preference1 == 'something_tasty':
            if preference2 == 'sweet':
                image = 'sweet.webp'
                message += " Вот тебе подарок — мешочек конфет."
            else:
                image = 'dish.jpg'
                message += " Вот тебе подарок — праздничное блюдо."
        else:
            if preference2 == 'refined':
                image = 'gift.webp'
                message += " Вот тебе подарок — изысканный подарок."
            else:
                image = 'tree.webp'
                message += " Вот тебе подарок — красивая новогодняя ёлка."

        return render_template('lab9/final.html', message=message, image=image)
    except ValueError:
        return "Ошибка: возраст должен быть числом.", 400
    except Exception as e:
        return f"Произошла ошибка: {str(e)}", 500
    
@lab9.route('/lab9/reset')
def reset():
    session.clear()  # Очищаем все данные в сессии
    return redirect(url_for('lab9.index'))  # Перенаправляем на начальную страницу