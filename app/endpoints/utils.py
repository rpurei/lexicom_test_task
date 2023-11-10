from config import DEBUG
from app_logger import logger_output

from fastapi import HTTPException
from re import findall


def http_exception(error_message: str, error_level: int, error_code: int):
    logger_output(str(error_message), DEBUG, error_level)
    raise HTTPException(status_code=error_code, detail=error_message)


def phone_symbols_check(input_number: str) -> bool:
    finded_list = findall(r'^(?:(?:8|\+7)(?:[-() ]*\d){11}|(?:[-() ]*\d){5,11})$', input_number)
    return True if len(finded_list) > 0 else False


def russian_format_check(input_number: str) -> str:
    trimmed_number = input_number.replace("'", '').replace('"', '').replace('-', '').replace(' ', '')
    trimmed_number = trimmed_number.replace('(', '').replace(')', '').replace('+', '')
    if trimmed_number.startswith('7') or len(trimmed_number) <= 7:
        return trimmed_number
    elif trimmed_number.startswith('8'):
        return f'7{trimmed_number[1:]}'
    elif trimmed_number.startswith('4') and len(trimmed_number) > 7:
        return f'7{trimmed_number}'
    else:
        return ''
