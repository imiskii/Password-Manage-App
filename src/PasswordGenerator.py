##
# File: PasswordGenerator.py
# Brief: Password Generator for Password Manager
# Autor: Michal Ľaš

import random
import string
import secrets

class PW_Generator:
    def generate():
        # remove some special characters
        punctuation = ""
        for symbol in string.punctuation:
            if (symbol != "`" and symbol != "'" and symbol != '"'):
                punctuation += symbol
        
        # Create list of characters
        charlist = string.ascii_lowercase + \
                   string.ascii_uppercase + \
                   string.digits + \
                   punctuation
        
        # Generate random string
        new_pw = "".join((secrets.choice(charlist) for i in range(0, random.randint(10,19))))
        return new_pw