import json

import pytest

from tests import app


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def h_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

    return headers


@pytest.fixture
def h_student_2():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

    return headers


@pytest.fixture
def h_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }

    return headers


@pytest.fixture
def h_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }

    return headers


@pytest.fixture
def h_principal():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }

    return headers


@pytest.fixture
def h_principal_invalid():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 3434,
            'user_id': 5
        })
    }

    return headers


@pytest.fixture
def h_teacher_invalid():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 3434,
            'user_id': 3
        })
    }

    return headers


@pytest.fixture
def h_student_invalid():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 3434,
            'user_id': 1
        })
    }

    return headers


@pytest.fixture
def h_user_invalid():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 4343
        })
    }

    return headers
