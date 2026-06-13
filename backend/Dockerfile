FROM python:3.11-slim

WORKDIR /app

# Copy requirement list. Since we don't have a requirements.txt, we write one here.
RUN pip install fastapi uvicorn sqlalchemy psycopg2-binary websockets pydantic requests "passlib[bcrypt]" python-jose httpx python-multipart "bcrypt<4.0"

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
