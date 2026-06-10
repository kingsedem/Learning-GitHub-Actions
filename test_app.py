import pytest
import allure

from testdata import expected_responses, invalid_inputs

pytestmark = [pytest.mark.functional, pytest.mark.regression_test]

_EXPECTED = expected_responses()
_INVALID = invalid_inputs()
_INVALID_BACKOFFICE = expected_responses()["signup_invalid_backoffice_token"]
_EMPTY_BACKOFFICE = expected_responses()["signup_empty_backoffice_token"]
_EXPIRED_BACKOFFICE = expected_responses()["signup_expired_backoffice_token"]
_EXISTING_USER_REGISTRATION = expected_responses()["signup_existing_user"]


@allure.title("Test to verify signup rejects invalid email")
@allure.severity(allure.severity_level.CRITICAL)
def test_signup_with_invalid_email_returns_422_bad_request_error(
    respondent_client, respondent_registration_with_invalid_email_payload, backoffice_access_token
):
    response = respondent_client.register_respondent(
        respondent_registration_with_invalid_email_payload, backoffice_access_token
    )
    expected = _EXPECTED["signup_invalid_email"]

    assert response.status_code == expected.status
    assert response.json().get("title") == expected.title




@allure.title("Test to verify signup rejects empty email")
@allure.severity(allure.severity_level.CRITICAL)
def test_signup_with_empty_email_returns_422_bad_request_error(
    respondent_client, respondent_registration_with_empty_email_payload, backoffice_access_token
):
    response = respondent_client.register_respondent(
        respondent_registration_with_empty_email_payload, backoffice_access_token
    )
    expected = _EXPECTED["signup_empty_email"]

    assert response.status_code == expected.status
    assert response.json().get("title") == expected.title



@allure.title("Test to verify signup rejects empty password")
@allure.severity(allure.severity_level.CRITICAL)
def test_signup_with_empty_password_returns_422_bad_request_error(
    respondent_client, respondent_registration_with_empty_password_payload, backoffice_access_token
):
    response = respondent_client.register_respondent(
        respondent_registration_with_empty_password_payload, backoffice_access_token
    )
    expected = _EXPECTED["signup_empty_password"]

    assert response.status_code == expected.status
    assert response.json().get("title") == expected.title



@allure.title("Test to verify signup rejects password as numbers only")
@allure.severity(allure.severity_level.CRITICAL)
def test_signup_with_password_as_only_numbers_returns_422_bad_request_error(
    respondent_client,
    respondent_registration_with_password_as_numbers_payload,
    backoffice_access_token,
):
    response = respondent_client.register_respondent(
        respondent_registration_with_password_as_numbers_payload, backoffice_access_token
    )
    expected = _EXPECTED["signup_numeric_password"]

    assert response.status_code == expected.status
    assert response.json().get("title") == expected.title




@allure.title("Test to verify signup rejects invalid backoffice token")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "invalid_backoffice_access_token",
    [
        pytest.param(_INVALID.invalid_backoffice_access_token, id="invalid_backoffice_access_token")
    ]
)
def test_signup_with_invalid_backoffice_token_returns_401_unauthorized_error(
    respondent_client,
    respondent_registration_payload,
    invalid_backoffice_access_token,
):
    response = respondent_client.register_respondent(
        respondent_registration_payload, invalid_backoffice_access_token
    )
    print(response.json())

    assert response.status_code == _INVALID_BACKOFFICE.status
    assert response.json().get("title") == _INVALID_BACKOFFICE.title



@allure.title("Test to verify signup rejects empty backoffice token")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "empty_backoffice_access_token",
    [
        pytest.param(_INVALID.empty_backoffice_access_token, id="empty_backoffice_access_token")
    ]
)
def test_signup_with_empty_backoffice_token_returns_401_unauthorized_error(
    respondent_client,
    respondent_registration_payload,
    empty_backoffice_access_token,
):
    response = respondent_client.register_respondent(
        respondent_registration_payload, empty_backoffice_access_token
    )
    print(response.json())

    assert response.status_code == _EMPTY_BACKOFFICE.status
    assert response.json().get("title") == _EMPTY_BACKOFFICE.title




@allure.title("Test to verify signup rejects expired backoffice token")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "expired_backoffice_access_token",
    [
        pytest.param(_INVALID.expired_backoffice_access_token, id="expired_backoffice_access_token")
    ]
)
def test_signup_with_expired_backoffice_token_returns_401_unauthorized_error(
    respondent_client,
    respondent_registration_payload,
    expired_backoffice_access_token,
):
    response = respondent_client.register_respondent(
        respondent_registration_payload, expired_backoffice_access_token
    )
    print(response.json())

    assert response.status_code == _EXPIRED_BACKOFFICE.status
    assert response.json().get("title") == _EXPIRED_BACKOFFICE.title


@allure.title("Test to verify signup rejects an already registered user")
@allure.severity(allure.severity_level.CRITICAL)
def test_signup_with_existing_user_account_returns_400_bad_request_error(
    respondent_client,
    respondent_registration_with_existing_user_payload,
    backoffice_access_token,
):
    response = respondent_client.register_respondent(
        respondent_registration_with_existing_user_payload, backoffice_access_token
    )
    print(response.json())

    assert response.status_code == _EXISTING_USER_REGISTRATION.status
    assert response.json().get("title") == _EXISTING_USER_REGISTRATION.title
