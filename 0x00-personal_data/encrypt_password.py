#!/usr/bin/env python3
"""
Encrypting and Checking valid password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypting  the given password and returns a salted hash"""
    # Generate a random salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the given password matches the hashed password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
