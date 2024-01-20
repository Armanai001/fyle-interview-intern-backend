# GET : student/assignments
def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_get_assignments_invalid_student(client, h_student_invalid):
    response = client.get(
        '/student/assignments',
        headers=h_student_invalid
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'Student not found'


def test_get_assignments_invalid_user(client, h_user_invalid):
    response = client.get(
        '/student/assignments',
        headers=h_user_invalid
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'User not found'


def test_get_assignments_teacher(client, h_teacher_1):
    response = client.get(
        '/student/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'requester should be a student'


def test_get_assignments_principal(client, h_principal):
    response = client.get(
        '/student/assignments',
        headers=h_principal
    )

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'requester should be a student'


# POST : student/assignment
def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


# def test_update_assignment_student_1(client, h_student_1):
#     content = 'ABCD TESTPOST'
#
#     response = client.post(
#         '/student/assignments',
#         headers=h_student_1,
#         json={
#             'id': 2,
#             'content': content
#         })
#
#     assert response.status_code == 200
#
#     data = response.json['data']
#     assert data['content'] == content
#     assert data['state'] == 'DRAFT'
#     assert data['teacher_id'] is None


def test_post_assignment_teacher(client, h_teacher_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_teacher_1,
        json={
            'content': content
        })

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'requester should be a student'


def test_post_assignment_principal(client, h_principal):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_principal,
        json={
            'content': content
        })

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'requester should be a student'


def test_post_assignment_invalid_user(client, h_user_invalid):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_user_invalid,
        json={
            'content': content
        })

    assert response.status_code == 403

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'User not found'


# POST : student/assignments/submit
def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_submit_assignment_teacher(client, h_teacher_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_teacher_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    error_response = response.json
    assert response.status_code == 403
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'requester should be a student'


def test_submit_assignment_principle(client, h_principal):
    response = client.post(
        '/student/assignments/submit',
        headers=h_principal,
        json={
            'id': 2,
            'teacher_id': 2
        })

    error_response = response.json
    assert response.status_code == 403
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'requester should be a student'


def test_submit_assignment_invalid_student(client, h_student_invalid):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_invalid,
        json={
            'id': 2,
            'teacher_id': 2
        })

    error_response = response.json
    assert response.status_code == 403
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'Student not found'


def test_submit_assignment_cross(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 3,
            'teacher_id': 2
        })

    assert response.status_code == 400

    data = response.json
    assert response.json['error'] == "FyleError"
    assert data['message'] == 'This assignment belongs to some other student'


def test_submit_assignment_bad_assignment(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 3433,
            'teacher_id': 2
        })

    assert response.status_code == 404

    error_response = response.json
    assert error_response['error'] == "FyleError"
    assert error_response['message'] == 'No assignment with this id was found'


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'
