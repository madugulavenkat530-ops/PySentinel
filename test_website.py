
from checks import WebsiteCheck
from unittest.mock import patch, Mock


@patch("checks.requests.get")
def test_website_returns_ok(mock_get):
    # Pretend the website returned HTTP 200
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    check = WebsiteCheck(["https://google.com"], 2000)

    results = check.run()

    assert results[0]["status"] == "OK"
    assert results[0]["status_code"] == 200


@patch("checks.requests.get")
def test_website_returns_fail_for_http_error(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    check = WebsiteCheck(["https://example.com"], 2000)

    results = check.run()

    assert results[0]["status"] == "FAIL"
    assert results[0]["status_code"] == 404
    assert results[0]["detail"] == "HTTP Error: 404"


@patch("checks.requests.get")
def test_website_returns_fail_on_timeout(mock_get):
    import requests

    mock_get.side_effect = requests.exceptions.Timeout

    check = WebsiteCheck(["https://slow-website.com"], 2000)

    results = check.run()

    assert results[0]["status"] == "FAIL"
    assert results[0]["detail"] == "Request timed out"


@patch("checks.requests.get")
def test_website_returns_fail_on_connection_error(mock_get):
    import requests

    mock_get.side_effect = requests.exceptions.ConnectionError

    check = WebsiteCheck(["https://offline-website.com"], 2000)

    results = check.run()

    assert results[0]["status"] == "FAIL"
    assert results[0]["detail"] == "Connection failed"


@patch("checks.requests.get")
def test_website_returns_warn_when_slow(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    check = WebsiteCheck(["https://slow-website.com"], 0)

    results = check.run()

    assert results[0]["status"] == "WARN"
