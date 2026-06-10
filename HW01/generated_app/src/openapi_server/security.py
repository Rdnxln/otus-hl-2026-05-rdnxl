import os
from   datetime         import datetime, timedelta, timezone
import jwt
from   fastapi          import HTTPException, Depends, status
from   fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from   sqlalchemy       import text

from   openapi_server.database import get_db # Импортируем наше подключение

import uuid

ACCESS_TOKEN_EXPIRE_MINUTES = 120 # Сессия на 5 минут
#ACCESS_TOKEN_EXPIRE_MINUTES = 120
# Секретный ключ для подписи токенов
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "some.super-secret/0password-phrase")
ALGORITHM = "HS256"

security_uuid = HTTPBearer()

async def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security_uuid)):
    if not credentials or credentials.scheme != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token scheme")

    token = credentials.credentials

    # Проверяем, является ли строка валидным UUID
    try:
        uuid.UUID(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not a valid UUID")

    # Проверяем наличие UUID в базе данных
    # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="TODO database token checking")
    # пока не вызываем исключение, не останавливаем обработку
    # проверку токена делаем в низовых методах
    # TODO: в дальнейшем можно сделать stateless-проверку валидности по формату JWT-токена
    # но мы следуем формату спецификации,
    # т.к. успешное обращение к эндпоинту login должно возвращать uuid

    async for db in get_db():
        # медленная авторизация по БД

        await db.execute( text("DELETE FROM sn_sess WHERE tact <= ( NOW() - INTERVAL '120 minutes' )") )
        await db.commit()

        # есть ли какая-нибудь информация в БД по сессии (токену)?
        # менее затратно извлечь 0, при наличии действующего токена
        query = text("""
 SELECT 0
 FROM   sn_sess
 WHERE  sess_id::varchar = :sess_id_param
""")

        result = await db.execute(query, { "sess_id_param": token } )
        row = result.fetchone() # Получаем одну строку
        # Если пользователь не найден
        if not row:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid")

        return {"service": "api_client", "auth_method": "UUID", "bearer_token": uuid.UUID(token) }

def create_access_jwt_token(user_id: str, sess_id: str) -> str:
    """Создает JWT токен (HTTP-сессию) для пользователя"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Payload — данные, которые зашиваем внутрь токена
    to_encode = {
        "sub": user_id, # Идентификатор субъекта (пользователя)
        "ses": sess_id, # Идентификатор сессии
        "exp": expire        # Время протухания сессии
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_jwt_token(token: str) -> str:
    """Проверяет токен и возвращает user_id. Если токен просрочен/неверен — кидает 401"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #user_id: str = payload.get("sub")
        sess_id: str = payload.get("ses")
        if sess_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидная сессия")
        return sess_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Сессия истекла, авторизуйтесь снова")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не удалось проверить сессию")
