import unittest
try:
    import utils
except ModuleNotFoundError:
    from .. import utils
import app


class TestTokenEncoder(unittest.TestCase):
    def test_encode_auth_token(self):
        response = utils.TokenEncoder.encode_auth_token('random', '123')
        self.assertEqual(response['status'], 'success')

    def test_decode_auth_token_invalid_token(self):
        invalid_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        output = utils.TokenEncoder.decode_auth_token(invalid_token)
        self.assertEqual(output, 'Invalid token. Please log in again.')

    def test_decode_auth_token_expired_token(self):
        expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTkzMjM1OTcsImlhdCI6MTU1OTMyMzU5NywibmFtZSI6Im1lb3ciLCJzdWIiOjN9.QpwRqCzhzX31nXWPuMuGNy03N77d-oYx3subJ0L8cSk'
        output = utils.TokenEncoder.decode_auth_token(expired_token)
        self.assertEqual(output, 'Signature expired. Please log in again.')

    def test_decode_auth_token_valid(self):
        valid_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTk0MDk5MTEsImlhdCI6MTU1OTMyMzUxMSwibmFtZSI6Im1lb3ciLCJzdWIiOjN9.pCvVy5WZJh3D0s3OFUflJGYE5Qdkubxr7wv8hf30jtQ'
        output = utils.TokenEncoder.decode_auth_token(valid_token)
        self.assertEqual(output['name'], 'meow')


class Test_get_json_data(unittest.TestCase):
    def setUp(self):
        self.app = app.create_app('config.TestingConfig').test_client()

    def test_correct_dict(self):
        test_dict = {
            'username': 'flask',
            'password': 'secret'
        }
        with self.app as c:
            c.get(
                '/api/igpost',
                json=test_dict
            )
            response = utils.get_json_data()
            self.assertEqual(response, test_dict)


if __name__ == '__main__':
    unittest.main()
