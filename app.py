import pytest
import allure


from models.respondent_payloads import REGISTRATION_QUALIFICATION_BUILDERS
from testdata import expected_responses, invalid_inputs
from dataclasses import replace

pytestmark = [pytest.mark.functional, pytest.mark.regression_test]

_INVALID = invalid_inputs()
_EXPECTED_RESPONSE_INVALID_QUALIFICATION_ID = expected_responses()["set_profile_invalid_qualifications_id"]
_EXPECTED_RESPONSE_EMPTY_QUALIFICATION_ID = expected_responses()["set_profile_empty_qualifications_id"]
_EXPECTED_RESPONSE_INVALID_S54_ACCESS_TOKEN = expected_responses()["login_invalid_survey54_access_token"]
_EXPECTED_RESPONSE_EMPTY_S54_ACCESS_TOKEN = expected_responses()["login_empty_survey54_access_token"]



@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "invalid_qualifications_id",
    [
        pytest.param(_INVALID.invalid_qualifications_id, id="invalid_qualifications_id")
    ]
)

@pytest.mark.parametrize(
    "build_qualification",
    REGISTRATION_QUALIFICATION_BUILDERS,
    ids=lambda builder: builder.__name__
)

def test_set_workflow_with_invalid_qualifications_id_returns_404_not_found_error(
    respondent_client, valid_respondent_access_token, build_qualification, invalid_qualifications_id, request
):
    allure.dynamic.title(f"Test to verify workflow registration rejects {request.node.callspec.id}")
    payload = build_qualification()
    # Because I already have a payload and just want to swap the ID
    payload = replace(payload, qualification_id=invalid_qualifications_id)

    response = respondent_client.add_workflow_qualification(
        payload, valid_respondent_access_token
    )
    print(response.json())

    assert response.status_code == _EXPECTED_RESPONSE_INVALID_QUALIFICATION_ID.status
    assert response.json()["title"] == _EXPECTED_RESPONSE_INVALID_QUALIFICATION_ID.title




@allure.severity(allure.severity_level.CRITICAL)

@pytest.mark.parametrize(
    "empty_qualifications_id",
    [
        pytest.param(_INVALID.empty_qualifications_id, id="empty_qualifications_id"),

    ]
)

@pytest.mark.parametrize(
    "build_qualification",
    REGISTRATION_QUALIFICATION_BUILDERS,
    ids=lambda builder: builder.__name__
)

def test_set_workflow_with_empty_qualifications_id_returns_422_error(
    respondent_client, valid_respondent_access_token, build_qualification, empty_qualifications_id, request
):
    allure.dynamic.title(f"Test to verify workflow registration rejects {request.node.callspec.id}")

    payload = build_qualification()
    # Because I already have a payload and just want to swap the ID
    payload = replace(payload, qualification_id=empty_qualifications_id)

    response = respondent_client.add_workflow_qualification(
        payload, valid_respondent_access_token
    )
    print(response.json())


    assert response.status_code ==  _EXPECTED_RESPONSE_EMPTY_QUALIFICATION_ID.status
    assert response.json()["title"] == _EXPECTED_RESPONSE_EMPTY_QUALIFICATION_ID.title





@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "invalid_survey54_access_token",
    [
        pytest.param(_INVALID.invalid_survey54_access_token, id="invalid_survey54_access_token")
    ]
)

@pytest.mark.parametrize(
    "build_qualification",
    REGISTRATION_QUALIFICATION_BUILDERS,
    ids=lambda builder: builder.__name__
)

def test_workflow_setup_invalid_access_token_returns_401_unauthorized_error(
    respondent_client, invalid_survey54_access_token, build_qualification, request
):  
    allure.dynamic.title(f"Test to verify workflow registration rejects {request.node.callspec.id}")

    response = respondent_client.add_workflow_qualification(
        build_qualification(), invalid_survey54_access_token
    )
    print(response.json())


    assert response.status_code ==  _EXPECTED_RESPONSE_INVALID_S54_ACCESS_TOKEN.status
    assert response.json()["title"] == _EXPECTED_RESPONSE_INVALID_S54_ACCESS_TOKEN.title



@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "empty_survey54_access_token",
    [
        pytest.param(_INVALID.empty_survey54_access_token, id="empty_survey54_access_token")
    ]
)

@pytest.mark.parametrize(
    "build_qualification",
    REGISTRATION_QUALIFICATION_BUILDERS,
    ids=lambda builder: builder.__name__
)

def test_workflow_setup_empty_access_token_returns_401_unauthorized_error(
    respondent_client, empty_survey54_access_token, build_qualification, request
):
    allure.dynamic.title(f"Test to verify workflow registration rejects {request.node.callspec.id}")

    response = respondent_client.add_workflow_qualification(
        build_qualification(), empty_survey54_access_token
    )
    print(response.json())

    assert response.status_code ==  _EXPECTED_RESPONSE_EMPTY_S54_ACCESS_TOKEN.status
    assert response.json()["title"] == _EXPECTED_RESPONSE_EMPTY_S54_ACCESS_TOKEN.title
