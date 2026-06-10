# coding: utf-8

from   typing import Dict, List  # noqa: F401

import importlib
import pkgutil

from   openapi_server.apis.default_api_base import BaseDefaultApi
import openapi_server.impl
from   fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from   openapi_server.security import verify_bearer_token

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictStr
from typing import Any, List, Optional, Union
from typing_extensions import Annotated
from openapi_server.models.dialog_message import DialogMessage
from openapi_server.models.dialog_user_id_send_post_request import DialogUserIdSendPostRequest
from openapi_server.models.login_post200_response import LoginPost200Response
from openapi_server.models.login_post500_response import LoginPost500Response
from openapi_server.models.login_post_request import LoginPostRequest
from openapi_server.models.post import Post
from openapi_server.models.post_create_post_request import PostCreatePostRequest
from openapi_server.models.post_update_put_request import PostUpdatePutRequest
from openapi_server.models.user import User
from openapi_server.models.user_register_post200_response import UserRegisterPost200Response
from openapi_server.models.user_register_post_request import UserRegisterPostRequest
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)

#@router.get("/api/protected")
#def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
#    token = credentials.credentials
#    return {"message": "Успешно!", "token": token}

@router.post(
    "/login",
    responses={
        200: {"model": LoginPost200Response, "description": "Успешная аутентификация"},
        400: {"description": "Невалидные данные"},
        404: {"description": "Пользователь не найден"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def login_post(
    login_post_request: Optional[LoginPostRequest] = Body(None, description=""),
) -> LoginPost200Response:
    """Упрощенный процесс аутентификации путем передачи идентификатор пользователя и получения токена для дальнейшего прохождения авторизации"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().login_post(login_post_request)


@router.post(
    "/user/register",
    responses={
        200: {"model": UserRegisterPost200Response, "description": "Успешная регистрация"},
        400: {"description": "Невалидные данные"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def user_register_post(
    user_register_post_request: Optional[UserRegisterPostRequest] = Body(None, description=""),
) -> UserRegisterPost200Response:
    """Регистрация нового пользователя"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().user_register_post(user_register_post_request)


@router.get(
    "/user/get/{id}",
    responses={
        200: {"model": User, "description": "Успешное получение анкеты пользователя"},
        400: {"description": "Невалидные данные"},
        404: {"description": "Анкета не найдена"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def user_get_id_get(
    id: Annotated[StrictStr, Field(description="Идентификатор пользователя")] = Path(..., description="Идентификатор пользователя"),
    auth_info: dict = Depends(verify_bearer_token),
) -> User:
    """Получение анкеты пользователя"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().user_get_id_get(id, auth_info)


@router.get(
    "/user/search",
    responses={
        200: {"model": List[User], "description": "Успешные поиск пользователя"},
        400: {"description": "Невалидные данные"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def user_search_get(
    first_name: Annotated[StrictStr, Field(description="Условие поиска по имени")] = Query(None, description="Условие поиска по имени", alias="first_name"),
    last_name: Annotated[StrictStr, Field(description="Условие поиска по фамилии")] = Query(None, description="Условие поиска по фамилии", alias="last_name"),
) -> List[User]:
    """Поиск анкет"""
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().user_search_get(first_name, last_name)


@router.put(
    "/friend/set/{user_id}",
    responses={
        200: {"description": "Пользователь успешно указал своего друга"},
        400: {"description": "Невалидные данные ввода"},
        401: {"description": "Неавторизованный доступ"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def friend_set_user_id_put(
    user_id: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().friend_set_user_id_put(user_id)


@router.put(
    "/friend/delete/{user_id}",
    responses={
        200: {"description": "Пользователь успешно удалил из друзей пользователя"},
        400: {"description": "Невалидные данные ввода"},
        401: {"description": "Неавторизованный доступ"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def friend_delete_user_id_put(
    user_id: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().friend_delete_user_id_put(user_id)


@router.post(
    "/post/create",
    responses={
        200: {"model": str, "description": "Успешно создан пост"},
        400: {"description": "Невалидные данные ввода"},
        401: {"description": "Неавторизованный доступ"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def post_create_post(
    post_create_post_request: Optional[PostCreatePostRequest] = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> str:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().post_create_post(post_create_post_request)


@router.put(
    "/post/update",
    responses={
        200: {"description": "Успешно изменен пост"},
        400: {"description": "Невалидные данные ввода"},
        401: {"description": "Неавторизованный доступ"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def post_update_put(
    post_update_put_request: Optional[PostUpdatePutRequest] = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().post_update_put(post_update_put_request)


@router.put(
    "/post/delete/{id}",
    responses={
        200: {"description": "Успешно удален пост"},
        400: {"description": "Невалидные данные ввода"},
        401: {"description": "Неавторизованный доступ"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def post_delete_id_put(
    id: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().post_delete_id_put(id)


@router.get(
    "/post/get/{id}",
    responses={
        200: {"model": Post, "description": "Успешно получен пост"},
        400: {"description": "Невалидные данные ввода"},
        401: {"description": "Неавторизованный доступ"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def post_get_id_get(
    id: StrictStr = Path(..., description=""),
) -> Post:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().post_get_id_get(id)


@router.get(
    "/post/feed",
    responses={
        200: {"model": List[Post], "description": "Успешно получены посты друзей"},
        400: {"description": "Невалидные данные ввода"},
        401: {"description": "Неавторизованный доступ"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def post_feed_get(
    offset: Optional[Union[Annotated[float, Field(strict=True, ge=0)], Annotated[int, Field(strict=True, ge=0)]]] = Query(0, description="", alias="offset"),
    limit: Optional[Union[Annotated[float, Field(strict=True, ge=1)], Annotated[int, Field(strict=True, ge=1)]]] = Query(10, description="", alias="limit"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[Post]:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().post_feed_get(offset, limit)


@router.post(
    "/dialog/{user_id}/send",
    responses={
        200: {"description": "Успешно отправлено сообщение"},
        400: {"description": "Невалидные данные ввода"},
        401: {"description": "Неавторизованный доступ"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def dialog_user_id_send_post(
    user_id: StrictStr = Path(..., description=""),
    dialog_user_id_send_post_request: Optional[DialogUserIdSendPostRequest] = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().dialog_user_id_send_post(user_id, dialog_user_id_send_post_request)


@router.get(
    "/dialog/{user_id}/list",
    responses={
        200: {"model": List[DialogMessage], "description": "Диалог между двумя пользователями"},
        400: {"description": "Невалидные данные ввода"},
        401: {"description": "Неавторизованный доступ"},
        500: {"model": LoginPost500Response, "description": "Ошибка сервера"},
        503: {"model": LoginPost500Response, "description": "Ошибка сервера"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def dialog_user_id_list_get(
    user_id: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[DialogMessage]:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().dialog_user_id_list_get(user_id)
