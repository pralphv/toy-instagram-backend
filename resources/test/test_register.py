import unittest

try:
    import register
except ModuleNotFoundError:
    from .. import register

import app


# class Test_check_user_in_database(unittest.TestCase):
#     def test_in_database(self):
        # self.assertTrue(ig_post.allowed_file('a.jpg'))

    # def test_not_in_database(self):
        # self.assertTrue(ig_post.allowed_file('a.jpg'))


class Test_check_same_password(unittest.TestCase):
    def test_same(self):
        self.assertTrue(
            register.RegisterResource.check_same_password('a', 'a')
        )

    def test_not_same(self):
        self.assertTrue(
            ~register.RegisterResource.check_same_password('a', 'b')
        )


class TestIgPostResource(unittest.TestCase):
    def setUp(self):
        self.app = app.create_app('config.TestingConfig').test_client()
        self.test_username = 'test'
        self.test_password = '123'

    def test_a_post_wrong_retype_password(self):
        json_ = {
            'username': self.test_username,
            'password': self.test_password,
            'retype_password': '321'
        }
        with self.app as c:
            response = c.post(
                '/api/register',
                json=json_,
            )
            self.assertIn('Password not same', response.data.decode('utf-8'))

    def test_b_post_valid_data(self):
        json_ = {
            'username': self.test_username,
            'password': self.test_password,
            'retype_password': self.test_password
        }
        with self.app as c:
            response = c.post(
                '/api/register',
                json=json_,
            )
            self.assertIn('success', response.data.decode('utf-8'))

    def test_c_post_user_exists(self):
        json_ = {
            'username': self.test_username,
            'password': self.test_password,
            'retype_password': self.test_password
        }
        with self.app as c:
            response = c.post(
                '/api/register',
                json=json_,
            )
            self.assertIn('User already exists', response.data.decode('utf-8'))

    def test_delete(self):
        """
        Please run after post request which creates a new database row
        """
        with self.app as c:
            response = c.delete(
                '/api/register',
                json={'username': self.test_username},
            )
            self.assertIn('success', response.data.decode('utf-8'))



if __name__ == '__main__':
    unittest.main()
