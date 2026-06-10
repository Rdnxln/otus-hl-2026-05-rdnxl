# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import Any, List, Optional, Union  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.dialog_message import DialogMessage  # noqa: F401
from openapi_server.models.dialog_user_id_send_post_request import DialogUserIdSendPostRequest  # noqa: F401
from openapi_server.models.login_post200_response import LoginPost200Response  # noqa: F401
from openapi_server.models.login_post500_response import LoginPost500Response  # noqa: F401
from openapi_server.models.login_post_request import LoginPostRequest  # noqa: F401
from openapi_server.models.post import Post  # noqa: F401
from openapi_server.models.post_create_post_request import PostCreatePostRequest  # noqa: F401
from openapi_server.models.post_update_put_request import PostUpdatePutRequest  # noqa: F401
from openapi_server.models.user import User  # noqa: F401
from openapi_server.models.user_register_post200_response import UserRegisterPost200Response  # noqa: F401
from openapi_server.models.user_register_post_request import UserRegisterPostRequest  # noqa: F401


def test_login_post(client: TestClient):
    """Test case for login_post

    
    """
    login_post_request = openapi_server.LoginPostRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/login",
    #    headers=headers,
    #    json=login_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_user_register_post(client: TestClient):
    """Test case for user_register_post

    
    """
    user_register_post_request = openapi_server.UserRegisterPostRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/user/register",
    #    headers=headers,
    #    json=user_register_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_user_get_id_get(client: TestClient):
    """Test case for user_get_id_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/user/get/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_user_search_get(client: TestClient):
    """Test case for user_search_get

    
    """
    params = [("first_name", 'Конст'),     ("last_name", 'Оси')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/user/search",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_friend_set_user_id_put(client: TestClient):
    """Test case for friend_set_user_id_put

    
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/friend/set/{user_id}".format(user_id='user_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_friend_delete_user_id_put(client: TestClient):
    """Test case for friend_delete_user_id_put

    
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/friend/delete/{user_id}".format(user_id='user_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_create_post(client: TestClient):
    """Test case for post_create_post

    
    """
    post_create_post_request = openapi_server.PostCreatePostRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/post/create",
    #    headers=headers,
    #    json=post_create_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_update_put(client: TestClient):
    """Test case for post_update_put

    
    """
    post_update_put_request = openapi_server.PostUpdatePutRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/post/update",
    #    headers=headers,
    #    json=post_update_put_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_delete_id_put(client: TestClient):
    """Test case for post_delete_id_put

    
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/post/delete/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_get_id_get(client: TestClient):
    """Test case for post_get_id_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/post/get/{id}".format(id='id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_feed_get(client: TestClient):
    """Test case for post_feed_get

    
    """
    params = [("offset", 0),     ("limit", 10)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/post/feed",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_dialog_user_id_send_post(client: TestClient):
    """Test case for dialog_user_id_send_post

    
    """
    dialog_user_id_send_post_request = openapi_server.DialogUserIdSendPostRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/dialog/{user_id}/send".format(user_id='user_id_example'),
    #    headers=headers,
    #    json=dialog_user_id_send_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_dialog_user_id_list_get(client: TestClient):
    """Test case for dialog_user_id_list_get

    
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/dialog/{user_id}/list".format(user_id='user_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

