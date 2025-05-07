from fastapi import HTTPException, status



UserErrorCreate = HTTPException(
    status_code=status.HTTP_502_BAD_GATEWAY, 
    detail="Ошибка создания пользователя"
)

UserAlreadyExist = HTTPException(
    status_code=status.HTTP_409_CONFLICT, 
    detail="Пользователь с таким логином уже существует"
)

UserIsNotPresent = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Не представлен"
)

IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail='Неверный формат токена',
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail='Токен отсутствует',
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail='Вы не авторизованы',
)

IncorrectUsernameOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail='Неверный логин или пароль',
)