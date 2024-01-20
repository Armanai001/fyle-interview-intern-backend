from core.models.assignments import AssignmentStateEnum, GradeEnum


# /teachers/assignments
def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_get_assignments_invalid_teacher(client, h_teacher_invalid):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_invalid
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'Teacher not found'


def test_get_assignments_invalid_user(client, h_user_invalid):
    response = client.get(
        '/teacher/assignments',
        headers=h_user_invalid
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'User not found'


def test_get_assignments_student(client, h_student_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_student_1
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'requester should be a teacher'


def test_get_assignments_principal(client, h_principal):
    response = client.get(
        '/teacher/assignments',
        headers=h_principal
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'requester should be a teacher'


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


# /teachers/assignments/grade
def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment(client, h_teacher_2):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 2,
            "grade": "B"
        }
    )
    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_regrade_assignment(client, h_teacher_2):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 2,
            "grade": "C"
        }
    )
    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_grade_assignment_invalid_User(client, h_user_invalid):
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_user_invalid,
        json={
            "id": 2,
            "grade": "C"
        }
    )
    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'User not found'
