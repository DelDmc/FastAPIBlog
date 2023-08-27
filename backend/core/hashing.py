from passlib.context import CryptContext

pwd_context = CryptContext(scheme=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_pass, hashed_pass):
        return pwd_context.verify(plain_pass, hashed_pass)
    
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)