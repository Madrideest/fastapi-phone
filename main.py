from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import phonenumbers
from phonenumbers import geocoder, carrier

app = FastAPI(
    title="Phone Formatter API",
    description="Форматирует номер телефона и возвращает информацию",
    version="1.0"
)

class PhoneRequest(BaseModel):
    phone: str = Field(..., example="89261234567", description="Телефонный номер в любом формате")

class PhoneResponse(BaseModel):
    formatted: str
    country: str
    carrier: str

@app.post("/format", response_model=PhoneResponse, summary="Форматировать номер телефона")
async def format_phone(data: PhoneRequest):
    phone = data.phone.strip()

    # Если номер не начинается с "+" — обрабатываем как российский
    if not phone.startswith('+'):
        if phone.startswith('8'):
            phone = '+7' + phone[1:]
        elif phone.startswith('9'):
            phone = '+7' + phone
        else:
            phone = '+' + phone

    try:
        number = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(number):
            return JSONResponse(content={"error": "Номер невалиден"}, status_code=400)

        return {
            "formatted": f"{number.country_code}-{number.national_number}",
            "country": geocoder.region_code_for_number(number),
            "carrier": carrier.name_for_number(number, "en")
        }
    except phonenumbers.NumberParseException:
        return JSONResponse(content={"error": "Ошибка парсинга номера"}, status_code=400)