import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import httplib2
from googleapiclient.errors import HttpError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import youtube_scheduled_upload as y


def error(status):
    return HttpError(httplib2.Response({'status': str(status)}), b'{"error":{"message":"rejected"}}')


class UploadRecoveryTests(unittest.TestCase):
    def run_upload(self, outcomes, duplicate=None, identity_error=None):
        with TemporaryDirectory() as root:
            token = Path(root) / 'token.json'
            token.write_text('{}')
            creds = MagicMock(expired=False, refresh_token='present')
            creds.to_json.return_value = '{}'
            yt = MagicMock()
            requests = [MagicMock() for _ in outcomes]
            for req, outcome in zip(requests, outcomes):
                req.next_chunk.side_effect = [outcome] if isinstance(outcome, Exception) else None
                if not isinstance(outcome, Exception):
                    req.next_chunk.return_value = (None, {'id': outcome})
            yt.videos.return_value.insert.side_effect = requests
            identity = identity_error if isinstance(identity_error, list) else ([identity_error, None] if identity_error else None)
            with patch.object(y.Credentials, 'from_authorized_user_info', return_value=creds), \
                 patch.object(y, 'build', return_value=yt), \
                 patch.object(y, 'verify_expected_channel', side_effect=identity), \
                 patch.object(y, 'check_episode_already_uploaded', side_effect=[(None, None), (duplicate, 'EP121')] if duplicate else None, return_value=(None, None)), \
                 patch.object(y, 'MediaFileUpload'), patch.object(y.time, 'sleep'):
                result = y.upload_to_youtube(token, 'EP121', '', [], 'video.mp4', {}, episode_number=121)
            return result, yt, creds

    def test_gone_session_restarts(self):
        result, yt, _ = self.run_upload([error(410), 'video'])
        self.assertEqual(result, 'video')
        self.assertEqual(yt.videos.return_value.insert.call_count, 2)

    def test_completed_attempt_does_not_create_duplicate(self):
        result, yt, _ = self.run_upload([error(410)], duplicate='existing')
        self.assertEqual(result, 'existing')
        self.assertEqual(yt.videos.return_value.insert.call_count, 1)

    def test_unexpired_rejected_token_refreshes(self):
        result, _, creds = self.run_upload(['video'], identity_error=error(401))
        self.assertEqual(result, 'video')
        creds.refresh.assert_called_once()

    def test_new_token_rejection_is_bounded_and_retried(self):
        result, _, creds = self.run_upload(['video'], identity_error=[error(401), error(401), None])
        self.assertEqual(result, 'video')
        self.assertEqual(creds.refresh.call_count, 2)

    def test_repeated_auth_failure_stops(self):
        with self.assertRaises(HttpError):
            self.run_upload(['video'], identity_error=[error(401), error(401), error(401)])

    def test_session_auth_failure_refreshes(self):
        result, _, creds = self.run_upload([error(401), 'video'])
        self.assertEqual(result, 'video')
        creds.refresh.assert_called_once()

    def test_restart_limit(self):
        with self.assertRaises(HttpError):
            self.run_upload([error(410), error(410), error(410)])

    def test_permission_error_is_not_retried(self):
        with self.assertRaises(HttpError):
            self.run_upload([error(403)])


if __name__ == '__main__':
    unittest.main()
