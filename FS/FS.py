from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import socket

app = FastAPI()

class RegisterRequest(BaseModel):
    hostname: str
    ip: str
    as_ip: str
    as_port: int

@app.put("/register")
def register_service(request: RegisterRequest):
    try:

        message = f"TYPE=A\nNAME={request.hostname}\nVALUE={request.ip}\nTTL=10\n"

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (request.as_ip, request.as_port)
        sock.sendto(message.encode(), server_address)
        
        return {"message": "Registration successful"}, 201
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.get("/fibonacci")
def get_fibonacci(number: int):
    if number < 0:
        raise HTTPException(status_code=400, detail="Number must be a non-negative integer")

    def fibonacci(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b
    
    result = fibonacci(number)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)