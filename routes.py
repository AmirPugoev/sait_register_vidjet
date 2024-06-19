#routes.py
from msilib.schema import tables
from flask import render_template, request, redirect, url_for, session
from database import manage_database, register_user, get_table_data, get_tables
import database
from flask import jsonify

admin_credentials = {
    '1111': '1111'  # Замените '1111' на фактический пароль администратора
}

def create_routes(app):
    @app.route('/')
    def index():
        tables = database.get_tables()
        return render_template('enter.html', tables=tables)

    @app.route('/admin_login', methods=['GET', 'POST'])
    def admin_login():
        # Маршрут для входа администратора
        if request.method == 'POST':
            username = request.form.get('username')  # Получаем имя пользователя из формы
            password = request.form.get('password')  # Получаем пароль из формы
            if admin_credentials.get(username) == password:
                # Проверка логина и пароля администратора
                session['admin_logged_in'] = True  # Устанавливаем флаг входа в сессию
                return redirect(url_for('admin'))  # Перенаправление на страницу администратора
            else:
                return 'Invalid username or password'  # Сообщение об ошибке при неверном логине или пароле
        return render_template('admin_login.html')  # Отображение формы входа администратора

    @app.route('/admin')
    def admin():
        # Маршрут для страницы администратора
        if 'admin_logged_in' in session:
            tables = database.manage_database()
            return render_template('admin.html', tables=tables)
        else:
            return redirect(url_for('admin_login'))  # Перенаправление на страницу входа администратора, если не выполнен вход

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            full_name = request.form['full_name']
            email = request.form['email']
            phone_number = request.form['phone_number']
            table_name = request.form['table_name']
            event = request.form['event']
            # Регистрация пользователя
            register_user(full_name, email, phone_number, table_name, event)
            return redirect(url_for('index'))
        
        tables = database.get_tables()
        return render_template('register.html', tables=tables)
        
        tables = database.get_tables()
        return render_template('register.html', tables=tables)

    @app.route('/view_table', methods=['GET'])
    def view_table():
        table_name = request.args.get('table_name')
        columns, data = database.get_table_data(table_name)
        return render_template('enter.html', tables=tables, selected_table=table_name, columns=columns, data=data)

    @app.route('/add_event', methods=['POST'])
    def add_event():
        table_name = request.form['table_name']
        event = request.form['event']
        event_date = request.form['event_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        address = request.form['address']
        ticket_count = request.form['ticket_count']
        manage_database(table_name, event, event_date, start_time, end_time, address, ticket_count)
        return redirect(url_for('index'))
    
    @app.route('/get_table_columns', methods=['GET'])
    def get_table_columns():
        table_name = request.args.get('table_name')
        if table_name:
            columns, _ = database.get_table_data(table_name)
            return jsonify(columns=columns)
        return jsonify(columns=[])

    @app.route('/get_column_data', methods=['GET'])
    def get_column_data():
        table_name = request.args.get('table_name')
        column_name = request.args.get('column_name')
        if table_name and column_name:
            columns, data = database.get_table_data(table_name)
            column_data = [row[columns.index(column_name)] for row in data]
            return jsonify(column_data=column_data)
        return jsonify(column_data=[])
    
    @app.route('/get_event_column', methods=['GET'])
    def get_event_column():
        table_name = request.args.get('table_name')
        event_column = 'мероприятие'
        if table_name:
            columns, data = database.get_table_data(table_name)
            if event_column in columns:
                column_data = [row[columns.index(event_column)] for row in data]
                return jsonify(column_data=column_data)
        return jsonify(column_data=[])
