from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from dotenv import load_dotenv 
load_dotenv()
security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET")


async def auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        print("tokens here" , token);
        print("jwt secret here" , JWT_SECRET);
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        print("decoded here" , decoded);
        return {
            "user": decoded,
            "userId": decoded.get("id"),
            "role": decoded.get("role"),
        }

    except JWTError as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Token is not valid")
