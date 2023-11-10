from config import REDIS_URL, REDIS_PORT, APP_LOG_ERROR
from .models import UserModel
from .utils import russian_format_check, http_exception, phone_symbols_check
from .exceptions import UserNotFound, PhoneFormatWrong, UserExists

from fastapi import APIRouter, status
from aioredis import Redis

router = APIRouter(tags=['Lexicom Test API'], responses={404: {'detail': 'Not found'}})
redis_client = Redis(host=REDIS_URL, port=REDIS_PORT, db=0, password='TestPassword8738')


@router.get('/')
async def root():
    return {'message': 'Lexicom test API online!'}


@router.get('/check_data', response_model=UserModel)
async def get_data(phone: str = '') -> UserModel:
    try:
        if not phone_symbols_check(russian_format_check(phone)):
            raise PhoneFormatWrong('Phone number wrong format, allowed symbols: 0-9, "-", "()"')
        user_address = await redis_client.get(russian_format_check(phone))
        if not user_address:
            raise UserNotFound('User with specified phone number not founded')
        return UserModel(phone=russian_format_check(phone),
                         address=user_address)
    except UserNotFound as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_404_NOT_FOUND)
    except PhoneFormatWrong as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/write_data', status_code=status.HTTP_201_CREATED)
async def post_data(user_payload: UserModel):
    try:
        if not phone_symbols_check(russian_format_check(user_payload.phone)):
            raise PhoneFormatWrong('Phone number wrong format, allowed symbols: 0-9, "-", "()"')
        user_address = await redis_client.get(russian_format_check(user_payload.phone))
        if user_address:
            raise UserExists('User with specified phone number exists')
        await redis_client.set(russian_format_check(user_payload.phone), user_payload.address)
    except PhoneFormatWrong as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_422_UNPROCESSABLE_ENTITY)
    except UserExists as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_409_CONFLICT)
    except Exception as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/write_data', status_code=status.HTTP_204_NO_CONTENT)
async def put_data(user_payload: UserModel):
    try:
        if not phone_symbols_check(russian_format_check(user_payload.phone)):
            raise PhoneFormatWrong('Phone number wrong format, allowed symbols: 0-9, "-", "()"')
        user_address = await redis_client.get(user_payload.phone)
        if not user_address:
            raise UserNotFound('User with specified phone number not founded')
        await redis_client.set(russian_format_check(user_payload.phone), user_payload.address)
    except PhoneFormatWrong as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_422_UNPROCESSABLE_ENTITY)
    except UserNotFound as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_404_NOT_FOUND)
    except Exception as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/', status_code=status.HTTP_200_OK)
async def delete_data(phone: str = ''):
    try:
        if not phone_symbols_check(russian_format_check(phone)):
            raise PhoneFormatWrong('Phone number wrong format, allowed symbols: 0-9, "-", "()"')
        user_address = await redis_client.get(phone)
        if not user_address:
            raise UserNotFound('User with specified phone number not founded')
        await redis_client.unlink(russian_format_check(phone))
    except PhoneFormatWrong as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_422_UNPROCESSABLE_ENTITY)
    except UserNotFound as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_404_NOT_FOUND)
    except Exception as err:
        http_exception(str(err), APP_LOG_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)
