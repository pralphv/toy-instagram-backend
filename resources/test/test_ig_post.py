import io
import os
import unittest

try:
    import ig_post
except ModuleNotFoundError:
    from .. import ig_post

from config import IMG_PATH
import app


class Test_allowed_file(unittest.TestCase):
    def test_allowed_file(self):
        self.assertTrue(ig_post.allowed_file('a.jpg'))
        self.assertTrue(ig_post.allowed_file('a.png'))
        self.assertTrue(ig_post.allowed_file('a.jpeg'))
        self.assertTrue(~ig_post.allowed_file('a.qwe'))


class Test_rename_filename(unittest.TestCase):
    def test_rename_filename(self):
        expected_number = len(os.listdir(IMG_PATH))
        filename = 'test.jpg'
        filename = ig_post.rename_filename(filename)
        self.assertEqual('{}.jpg'.format(expected_number), filename)


class TestIgPostResource(unittest.TestCase):
    def setUp(self):
        self.app = app.create_app('config.TestingConfig').test_client()
        self.authorization = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTk0MDk5MTEsImlhdCI6MTU1OTMyMzUxMSwibmFtZSI6Im1lb3ciLCJzdWIiOjN9.pCvVy5WZJh3D0s3OFUflJGYE5Qdkubxr7wv8hf30jtQ'

    def test_get(self):
        with self.app as c:
            response = c.get(
                '/api/igpost',
            )
            self.assertIn('success', response.data.decode('utf-8'))

    def test_post(self):
        data = {
            'file': (io.BytesIO(b"abcdef"), 'test.jpg'),
            'test': True,
            'description': 'test'
        }
        with self.app as c:
            response = c.post(
                '/api/igpost',
                data=data,
                headers={'Authorization': self.authorization}
            )
            self.assertIn('success', response.data.decode('utf-8'))

    def test_delete(self):
        """
        Please run after post request which creates a new database row
        """
        expected_number = len(os.listdir(IMG_PATH))
        json_ = {
            'filename': '{}.jpg'.format(expected_number),
        }
        with self.app as c:
            response = c.delete(
                '/api/igpost',
                json=json_,
            )
            self.assertIn('success', response.data.decode('utf-8'))

    def test_post_no_file(self):
        data = {
            'test': True,
            'description': 'test'
        }
        with self.app as c:
            response = c.post(
                '/api/igpost',
                data=data,
                headers={'Authorization': self.authorization}
            )
            self.assertIn('no file', response.data.decode('utf-8'))

    def test_post_malformed_authorization(self):
        data = {
            'file': (io.BytesIO(b"abcdef"), 'test.jpg'),
            'test': True,
            'description': 'test'
        }
        with self.app as c:
            response = c.post(
                '/api/igpost',
                data=data,
                headers={'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleH1vrjE1NTk0MDk5MTEsImlhdCI6MTU1OTMyMzUxMSwibmFtZSI6Im1lb3ciLCJzdWIiOjN9.pCvVy5WZJh3D0s3OFUflJGYE5Qdkubxr7wv8hf30jtQ'}
            )
            self.assertIn('Invalid token', response.data.decode('utf-8'))

    def test_post_wrong_file_extension(self):
        data = {
            'file': (io.BytesIO(b"abcdef"), 'test.qwe'),
            'test': True,
            'description': 'test'
        }
        with self.app as c:
            response = c.post(
                '/api/igpost',
                data=data,
                headers={'Authorization': self.authorization}
            )
            self.assertIn('wrong file extension', response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
