"""Test the rayvision_api utils functions."""

# pylint: disable=import-error
import pytest

from rayvision_api import signature


def test_generate_nonce():
    """Test generate random Numbers for verification."""
    assert isinstance(signature.generate_nonce(), str)


def test_generate_timestamp():
    """Test generate the timestamp for verification."""
    assert isinstance(signature.generate_timestamp(), str)


def test_generate_signature():
    """Test we can get correct signature."""
    data = signature.generate_signature('test_key', 'test_msg')
    assert data == b'TC9wro8movj4HGMphrpEdES3oBdPsq+y+2tAt6kM/Tw='


def test_generate_header_body_str(header):
    """Test we can get correct header body strings.

    Make sure we get the correct headers structure, because there are strict
    requirements on the headers structure when requesting it.

    """
    results = '[POST]tests.com:api_url&UTCTimestamp=32166266&accessId=xxx&channel=4&key=value&nonce=1465&platform=2&version=dev'  # noqa: E501  # pylint: disable=line-too-long
    header_and_body = signature.generate_headers_body_str('tests.com',
                                                          'api_url',
                                                          header=header,
                                                          body={'key': 'value'})
    assert header_and_body == results


def test_headers_body_sort(header):
    """Test that we can get the correct headers sort."""
    sort_keys = list(
        signature.headers_body_sort(header, {'key': 'value'}).keys())
    assert sort_keys == ['UTCTimestamp',
                         'accessId',
                         'channel',
                         'key',
                         'nonce',
                         'platform',
                         'version']


@pytest.mark.parametrize('test_case,results', [
    ({'key_a': {'key_b': 'value_c'}}, {'key_a.key_b': 'value_c'}),
    ({'a': {'b': {'c': {'d': 'e'}}}}, {'a.b.c.d': 'e'}),
    ({'key_a': {'sub_key': [
        {'c': {'d': 1234}},
        {'test_key_a': {'test_key': ''}},
    ]}}, {'key_a.sub_key0.c.d': 1234,
          'key_a.sub_key1.test_key_a.test_key': ''})
])
def test_formatted_headers(test_case, results):
    """Test we can get the correct dictionary structure after formatting."""
    assert signature.formatted_headers(test_case) == results


@pytest.mark.parametrize('test_case,results', [
    ('MyKeyName', 'my_key_name'),
    ('myKeyname', 'my_keyname'),
    ('myKeyName', 'my_key_name')
])
def test_hump2underline(test_case, results):
    """Test we can get a correct result."""
    assert signature.hump2underline(test_case) == results
