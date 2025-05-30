import unittest
from main import app, users
from werkzeug.security import generate_password_hash, check_password_hash

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Включаем режим тестирования
        app.testing = True
        self.client = app.test_client()
        users.clear()  # Очищаем "базу данных" перед каждым тестом

    def test_register_success(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)

        self.assertIn('Вы успешно зарегистрировались!', response.data.decode('utf-8'))
        self.assertIn('testuser', users)
        self.assertTrue(check_password_hash(users['testuser'], 'testpass'))

    def test_register_existing_user(self):
        users['existinguser'] = generate_password_hash('123')
        response = self.client.post('/register', data={
            'username': 'existinguser',
            'password': 'any'
        }, follow_redirects=True)

        self.assertIn('Пользователь с таким именем уже существует!', response.data.decode('utf-8'))

    def test_login_success(self):
        users['validuser'] = generate_password_hash('secret')
        response = self.client.post('/login', data={
            'username': 'validuser',
            'password': 'secret'
        }, follow_redirects=True)

        self.assertIn('Вы успешно вошли в систему!', response.data.decode('utf-8'))

    def test_login_failure(self):
        users['user'] = generate_password_hash('correct')
        response = self.client.post('/login', data={
            'username': 'user',
            'password': 'wrong'
        }, follow_redirects=True)

        self.assertIn('Неправильное имя пользователя или пароль!', response.data.decode('utf-8'))

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<html', response.data.decode('utf-8').lower())  # Проверка на наличие HTML

if __name__ == '__main__':
    unittest.main()