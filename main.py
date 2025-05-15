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


def normalize_number(input_text: str) -> str:
    input_text = input_text.strip().replace(" ", "").replace("-", "")

    if input_text.startswith('+'):
        return input_text

    if input_text.startswith('8') and len(input_text) == 11:
        return '+7' + input_text[1:]  # заменяем первую 8 на +7 (Россия)

    # В остальных случаях просто добавляем +
    return '+' + input_text


@app.post("/format", response_model=PhoneResponse, summary="Форматировать номер телефона")
async def format_phone(data: PhoneRequest):
    phone_text = data.phone.strip()
    phone = normalize_number(phone_text)

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