from core.models.assignments import AssignmentStateEnum, GradeEnum


# /principal/assignments
def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/principal/assignments',
        headers=h_student_1
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'requester should be a principal'


def test_get_assignments_teacher(client, h_teacher_1):
    response = client.get(
        '/principal/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'requester should be a principal'


def test_get_assignments_student(client, h_student_1):
    response = client.get(
        '/principal/assignments',
        headers=h_student_1
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'requester should be a principal'


def test_get_assignments_invalid_principal(client, h_principal_invalid):
    response = client.get(
        '/principal/assignments',
        headers=h_principal_invalid
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'Principal not found'


def test_get_assignments_invalid_user(client, h_user_invalid):
    response = client.get(
        '/principal/assignments',
        headers=h_user_invalid
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'User not found'


# /principal/assignments/grade
def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


# /principal/assignments/grade
def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_grade_assignment_bad_grade(client, h_principal):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            "id": 4,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_invalid_principal(client, h_principal_invalid):
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal_invalid,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'Principal not found'


def test_grade_assignment_teacher(client, h_teacher_1):
    response = client.post(
        '/principal/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == "requester should be a principal"


def test_grade_assignment_student(client, h_student_1):
    response = client.post(
        '/principal/assignments/grade',
        headers=h_student_1,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == "requester should be a principal"


# /principal/teachers
def test_get_teachers_list(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200


def test_get_teachers_invalid_principal(client, h_principal_invalid):
    response = client.get(
        '/principal/teachers',
        headers=h_principal_invalid
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'Principal not found'


def test_get_teachers_teacher(client, h_teacher_1):
    response = client.get(
        '/principal/teachers',
        headers=h_teacher_1
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == "requester should be a principal"


def test_get_teachers_student(client, h_student_1):
    response = client.get(
        '/principal/teachers',
        headers=h_student_1
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == "requester should be a principal"


def test_get_teachers_invalid_user(client, h_user_invalid):
    response = client.get(
        '/principal/teachers',
        headers=h_user_invalid
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'User not found'
