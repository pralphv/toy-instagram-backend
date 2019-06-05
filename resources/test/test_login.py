import unittest

try:
    import login
    import register
except ModuleNotFoundError:
    from .. import login
    from .. import register

import app


class TestLoginResource(unittest.TestCase):
    def setUp(self):
        self.app = app.create_app('config.TestingConfig').test_client()
        self.username = 'testing'
        self.register()

    def register(self):
        json_ = {
            'username': self.username,
            'password': self.username,
            'retype_password': self.username
        }
        with self.app as c:
            c.post(
                '/api/register',
                json=json_,
            )

    def test_post_correct_password(self):
        json_ = {
            'username': self.username,
            'password': self.username,
        }
        with self.app as c:
            response = c.post(
                '/api/login',
                json=json_,
            )
            self.assertIn('success', response.data.decode('utf-8'))

    def test_post_incorrect_password(self):
        json_ = {
            'username': self.username,
            'password': '21321321',
        }
        with self.app as c:
            response = c.post(
                '/api/login',
                json=json_,
            )
            self.assertIn('wrong password', response.data.decode('utf-8'))

    def test_post_user_not_exists(self):
        json_ = {
            'username': 'meow',
            'password': '21321321',
        }
        with self.app as c:
            response = c.post(
                '/api/login',
                json=json_,
            )
            self.assertIn('user does not exist', response.data.decode('utf-8'))

    def test_z_tearDownClass(self):
        """
        Should be a teardown but fails with:
        tearDownClass() missing 1 required positional argument: 'self'
        Using a hacky way for now
        """
        with self.app as c:
            response = c.delete(
                '/api/register',
                json={'username': self.username},
            )
            self.assertIn('success', response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
