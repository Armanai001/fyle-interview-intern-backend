def test_get_invalid_page(client, h_student_1):
    response = client.get(
        '/random_url',
        headers=h_student_1
    )

    assert response.status_code == 404

    assert response.json['error'] == 'NotFound'
