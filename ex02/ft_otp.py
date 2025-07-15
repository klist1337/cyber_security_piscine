
import argparse
import time
from otp import TOTP


def main() :
    messageError = "ft_otp.py: error: key must be at least 64 hexadecimal characters"
    parser = argparse.ArgumentParser()

    parser.add_argument("-g", help="take hexadecimal key at " \
                                    "least 64 characters and save it in file called ft_otp.key")
    parser.add_argument("-k", help="Generates a new temporary password based on the key " \
                                    "given as argument and prints it on the standard output")
    args = parser.parse_args()

    if args.g: 
        try :
            # check Key arg length 
            if (len(args.g) < 64) :
                exit(messageError)
            
            #check if Key arg is hexa format 
            int(args.g, 16)
            filename = "ft_otp.key"
            
            with open(filename, 'x') as f:
                f.write(args.g)
                print(f"Key was successfull saved in {filename}")
        except ValueError :
            exit(messageError)
    elif args.k:

        with open(args.k, 'r') as f:
            hexa_str = f.read()
        try:
            #check len of key in the file
            if len(hexa_str) < 64:
                exit(messageError)

            #chek if key in the file are hexadecimal   
            int(hexa_str, 16)

            otp = TOTP()
            """
            get time window time 
            T = (temps Unix actuel - T0) // X we choose X = 30 T0 = 0
            """
            t = int(time.time() // 30)
            # convert time to. hexa  [2:]string start after first two character (remove 0x prefix)
            #rjust add O at the left to have 16 characters
            time_hex = hex(t)[2:].rjust(16, '0')

            code = otp.generateOTPSHA1(hexa_str, time_hex, "6")
            print(code)

        except ValueError:
            exit(messageError)
        
if __name__ == "__main__" :
    main()