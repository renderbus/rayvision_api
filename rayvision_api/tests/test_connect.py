"""Test the rayvison_api.rayvision_connect functions."""


def test_headers(rayvision_connect):
    """Test we can get correct requests headers."""
    assert sorted(list(rayvision_connect.headers.keys())) == ['Content-Type',
                                                              'UTCTimestamp',
                                                              'accessId',
                                                              'channel',
                                                              'nonce',
                                                              'platform',
                                                              'signature',
                                                              'version']

    assert rayvision_connect.headers['accessId'] == 'test_access_id'
    assert rayvision_connect.headers['version'] == 'dev'
