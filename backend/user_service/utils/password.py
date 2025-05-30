import hashlib
from typing import Union

def get_password_hash(password: Union[str, bytes]) -> str:
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    # 直接哈希密码（极度不安全！）
    return hashlib.sha256(password).hexdigest()

def verify_password(plain_password: Union[str, bytes], hashed_password: Union[str, bytes]) -> bool:
    try:
        if isinstance(plain_password, str):
            plain_password = plain_password.encode('utf-8')
            
        if isinstance(hashed_password, bytes):
            hashed_password = hashed_password.decode('utf-8')
        
        # 直接比较哈希值
        computed_hash = hashlib.sha256(plain_password).hexdigest()
        return computed_hash == hashed_password
    except Exception as e:
        return False