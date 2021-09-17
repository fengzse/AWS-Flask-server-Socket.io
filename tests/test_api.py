'''
import json
import unittest

from ..app import create_app


class TestClientCase(unittest.TestCase):
    # Create run time context for app
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    # Eliminate test environment
    def tearDown(self) -> None:
        self.app_context.pop()

    def test_send_message(self):
        msg_start = {
            'code': 1,
            'message': 'Recording starts',
        }

        msg_stop = {
            'code': 2,
            'message': 'Recording ends'
        }
        # simulate app-client posts to server, status code 201 expected
        response_post = self.client.post(('/api/v1.0/send/' + str(msg_start.get('code'))),
                                         data=json.dumps(msg_start), content_type='app/json')
        self.assertEqual(201, response_post.status_code)

        # simulate data has been accepted by server and responds, status code 200 expected
        # Location: api.get_user
        url = response_post.headers.get('Location')
        response_get = self.client.get(url)
        self.assertEqual(200, response_get.status_code)

        # assert the specific data responded by server is the one sent by app-client
        data = json.loads(response_get.get_data(as_text=True))
        self.assertEqual(msg_start.get('message'), data.get('action'))


if __name__ == '__main__':
    unittest.main()'''
