from typing     import Optional
from fastapi    import HTTPException, Request, status
from sqlalchemy import text

from openapi_server.security import create_access_jwt_token
from pydantic   import StrictStr

from openapi_server.database import get_db # Импортируем наше подключение
import hashlib
import uuid

# Импортируем базовый класс, который ищет роутер
from openapi_server.apis.default_api_base import BaseDefaultApi

# Импортируем модели данных, сгенерированные OpenAPI

# реализация /login
from openapi_server.models.login_post_request     import LoginPostRequest
from openapi_server.models.login_post200_response import LoginPost200Response

# реализация /user/register
from openapi_server.models.user_register_post_request     import UserRegisterPostRequest
from openapi_server.models.user_register_post200_response import UserRegisterPost200Response

# реализация /user/get/
from openapi_server.models.user import User

class DefaultApiImpl(BaseDefaultApi):
    """ Реализация методов бизнес-логики для BaseDefaultApi """

    # POST: /login
    async def login_post(
        self,
        login_post_request: Optional[LoginPostRequest] = None,
    ) -> LoginPost200Response:
        """ Логика аутентификации пользователя """

        # 1. Проверяем, что запрос не пустой
        if not login_post_request:
            raise HTTPException(status_code=400, detail="Тело запроса пустое")

        # Если строго следовать спецификации задания:
        # Имеем следующее, при регистрации возвращается user_id как uuid
        # поэтому, мы предполагаем, что в id ожидается uuid,
        # но пользователям неудобно оперировать uuid,
        # Поэтому, немного расширим модель (поле login в БД)
        username = login_post_request.id
        password = login_post_request.password

        async for db in get_db():

            await db.execute( text("DELETE FROM sn_sess WHERE tact <= ( NOW() - INTERVAL '120 minutes' )") )
            await db.commit()
            # :param для защиты от SQL-инъекций
            # учитываем время жизни сессии
            query = text("""
 SELECT password,
        user_id,
   ( SELECT sess_id
     FROM   sn_sess
     WHERE  user_id=sn_users.user_id
            AND tact > ( NOW() - INTERVAL '120 minutes' )
     ORDER BY tact DESC
     LIMIT 1
   )    sess_id
 FROM   sn_users
 WHERE  (               login = :username_param           -- параметр id интерпретируем как имя_пользователя
          OR user_id::varchar = :username_as_uuid_param ) -- параметр id интерпретируем как user_id
 LIMIT 1
            """)

            result = await db.execute( query,
                                       {"username_param": username,
                                        "username_as_uuid_param": username })
            row = result.fetchone() # Получаем одну строку

            # Если пользователь не найден
            if not row:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            db_password_hash = row[0]
            user_id          = row[1]
            sess_id          = row[2]

            pwd = str(user_id) + 'secret.salt' + password
            hash_obj = hashlib.md5(pwd.encode('utf-8'))
            pwd_hash = hash_obj.hexdigest()

            if db_password_hash != pwd_hash:
                raise HTTPException(status_code=401, detail="Неверный пароль")

            if not sess_id:
                sess_id = uuid.uuid4()
                result = await db.execute( text("INSERT INTO sn_sess VALUES ( :sess_id, :user_id, NOW() )"),
                                           { "sess_id" : sess_id, "user_id" : user_id } )
                if result.rowcount != 1:
                    raise HTTPException(status_code=500, detail="Внутренняя ошибка" )

                await db.commit()

            # Если всё успешно, генерируем и возвращаем ответ
            # access_token = create_access_jwt_token( str(user_id), str(sess_id) )
            access_token = str(sess_id)
            return LoginPost200Response(
                token=access_token
            )

    # POST: /user/register
    async def user_register_post(
        self,
        user_register_post_request: Optional[UserRegisterPostRequest] = None,
    ) -> UserRegisterPost200Response:
        """Регистрация нового пользователя"""

        # 1. Проверяем, что запрос не пустой
        if not user_register_post_request:
            raise HTTPException(status_code=400, detail="Тело запроса пустое")

        #username    = user_register_post_request.id
        password    = user_register_post_request.password
        first_name  = user_register_post_request.first_name
        second_name = user_register_post_request.second_name
        birthdate   = user_register_post_request.birthdate
        biography   = user_register_post_request.biography
        city        = user_register_post_request.city
        # sex         = user_register_post_requset.sex

        #print( "req="+str(user_register_post_request ) )

        async for db in get_db():

            await db.execute( text("DELETE FROM sn_sess WHERE tact <= ( NOW() - INTERVAL '120 minutes' )") )
            await db.commit()

            # Запрос пытается вставить город.
            # Если имя уже есть, он делает "фиктивный UPDATE", чтобы сработал RETURNING city_id
            query = text("""
 INSERT INTO sn_cities (city)
 VALUES (:city_name)
 ON CONFLICT (city)
 DO UPDATE SET city = EXCLUDED.city
 RETURNING city_id
                         """)

            result = await db.execute(query, {"city_name": city})
            city_id = result.scalar()  # Здесь всегда будет uuid или integer (в зависимости от структуры)
            await db.commit()
            #print(f"ID города '{city}': {city_id}")

            new_user_uuid = uuid.uuid4()
            query = text("""
 INSERT INTO sn_users
 ( user_id, login,
   first_name, second_name,
   birthdate,  biography,
   city_id,
   sex,
   password )
   VALUES
   ( :user_id_param, :login_param,
     :first_name_param, :second_name_param,
     :birthdate_param, :biography_param,
     :city_param,
     NULL, -- not implemented
     md5(:user_id_str_param || 'secret.salt' || :password_param )
   )
                         """)
            result = await db.execute(
              query,
              { "user_id_param" : new_user_uuid,
                "login_param" : str(new_user_uuid), # TODO: extend POST params for 'login'
                "first_name_param" : first_name,
                "second_name_param" : second_name,
                "birthdate_param" : birthdate,
                "biography_param" : biography,
                "city_param" : city_id,
              # "sex_param" : sex,
                "user_id_str_param" : str( new_user_uuid ),
                "password_param" : password
              }
            )
            await db.commit()
            return UserRegisterPost200Response(
            #    user_id=str("0000-00-00-0000")
                user_id=str(new_user_uuid)
            )

    # GET: /user/get/
    async def user_get_id_get(
        self,
        id:        StrictStr,
        auth_info: dict
    ) -> User:
        """Получение данных пользователя"""
        #print( "ID: " + str(id) )
        print( "auth_info " + str(auth_info) )
        print( "sess_id " + str(auth_info['bearer_token']) )
        async for db in get_db():

            # медленная авторизация по БД
            query = text("""
 SELECT user_id::varchar as id,
        first_name,
        second_name,
        birthdate,
        biography,
        ( SELECT city
          FROM   sn_cities
          WHERE  city_id = sn_users.city_id
        ) as city
 FROM   sn_users
 WHERE  user_id::varchar = :user_id_param
""")

            result = await db.execute(query, {"user_id_param": str(id)})
            user_data = result.mappings().first()  # Получаем обычный Row

            if not user_data:
                raise HTTPException(status_code=404, detail="Анкета не найдена")

            return User(**user_data)
