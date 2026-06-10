# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

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

class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def login_post(
        self,
        login_post_request: Optional[LoginPostRequest],
    ) -> LoginPost200Response:
        """Упрощенный процесс аутентификации путем передачи идентификатор пользователя и получения токена для дальнейшего прохождения авторизации"""
        ...


    async def user_register_post(
        self,
        user_register_post_request: Optional[UserRegisterPostRequest],
    ) -> UserRegisterPost200Response:
        """Регистрация нового пользователя"""
        ...


    async def user_get_id_get(
        self,
        id: Annotated[StrictStr, Field(description="Идентификатор пользователя")],
    ) -> User:
        """Получение анкеты пользователя"""
        ...


    async def user_search_get(
        self,
        first_name: Annotated[StrictStr, Field(description="Условие поиска по имени")],
        last_name: Annotated[StrictStr, Field(description="Условие поиска по фамилии")],
    ) -> List[User]:
        """Поиск анкет"""
        ...


    async def friend_set_user_id_put(
        self,
        user_id: StrictStr,
    ) -> None:
        ...


    async def friend_delete_user_id_put(
        self,
        user_id: StrictStr,
    ) -> None:
        ...


    async def post_create_post(
        self,
        post_create_post_request: Optional[PostCreatePostRequest],
    ) -> str:
        ...


    async def post_update_put(
        self,
        post_update_put_request: Optional[PostUpdatePutRequest],
    ) -> None:
        ...


    async def post_delete_id_put(
        self,
        id: StrictStr,
    ) -> None:
        ...


    async def post_get_id_get(
        self,
        id: StrictStr,
    ) -> Post:
        ...


    async def post_feed_get(
        self,
        offset: Optional[Union[Annotated[float, Field(strict=True, ge=0)], Annotated[int, Field(strict=True, ge=0)]]],
        limit: Optional[Union[Annotated[float, Field(strict=True, ge=1)], Annotated[int, Field(strict=True, ge=1)]]],
    ) -> List[Post]:
        ...


    async def dialog_user_id_send_post(
        self,
        user_id: StrictStr,
        dialog_user_id_send_post_request: Optional[DialogUserIdSendPostRequest],
    ) -> None:
        ...


    async def dialog_user_id_list_get(
        self,
        user_id: StrictStr,
    ) -> List[DialogMessage]:
        ...
