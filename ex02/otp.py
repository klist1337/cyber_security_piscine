
import hmac
import hashlib
class TOTP :
    DIGITS_POWER = [10**i for i in range(9)]

    @staticmethod
    def hexa_str_to_bytes(hex_str:str):
        if len(hex_str) % 2:
            hex_str = "0" + hex_str
        return bytes.fromhex(hex_str)
    
    @staticmethod
    def hma_sha(crypto, key_bytes, text_bytes):
        sha_funct = {
            "HmacSHA1": hashlib.sha1,
            "HmacSHA256": hashlib.sha256,
            "HmacSHA512": hashlib.sha512
        }.get(crypto)
        
        if sha_funct is None:
            raise ValueError("Unsupported crypto algorithm")

        return hmac.new(key_bytes, text_bytes, sha_funct).digest()
    
    @staticmethod
    def generateOTP(key_hex, time_hex, return_digits, crypto):
        """
        : param key_hex : secret key in hexadecimal 
        : param time_hex : temps en hexadecimal (16 characters: 8 bytes)
        : param return digits: number of digits to be returned
        : param crypto : Crypto algo to be used
        """
        codedigits = int(return_digits)
        
        # add 0 at left if it's neccessary
        time_hex = time_hex.rjust(16, '0')

        msg = TOTP.hexa_str_to_bytes(time_hex)
        k = TOTP.hexa_str_to_bytes(key_hex)

        hash_bytes = TOTP.hma_sha(crypto, k, msg)
        offset = hash_bytes[-1] & 0x0F

        # get binary with 31 bytes for otp with big endian
        binary = (
                ((hash_bytes[offset] & 0x7F) << 24) | 
                ((hash_bytes[offset + 1] & 0xFF) << 16) |
                ((hash_bytes[offset + 2] & 0xFF) << 8) |
                ((hash_bytes[offset + 3] & 0xFF)) 
            )
        otp = binary % TOTP.DIGITS_POWER[codedigits]

        return str(otp).zfill(codedigits)
    
    @staticmethod
    def generateOTPSHA1(key_hex, time_hex, return_digits):
        return TOTP.generateOTP(key_hex, time_hex, return_digits, "HmacSHA1")
    
    @staticmethod
    def generateOTPSHA256(key_hex, time_hex, return_digits):
        return TOTP.generateOTP(key_hex, time_hex, return_digits, "HmacSHA256")
    
    @staticmethod
    def generateOTPSHA512(key_hex, time_hex, return_digits):
        return TOTP.generateOTP(key_hex, time_hex, return_digits, "HmacSHA512")