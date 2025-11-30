"""
Script to generate RSA key pair for JWT authentication
Tạo private key cho auth_service (để ký token) và public key cho resource_service (để verify token)
"""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import os

def generate_rsa_keypair():
    """Generate RSA key pair"""
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Get public key
    public_key = private_key.public_key()
    
    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Create directories if they don't exist
    os.makedirs("auth_service/rsa_keys", exist_ok=True)
    os.makedirs("resource_service/rsa_keys", exist_ok=True)
    
    # Write private key to auth_service
    with open("auth_service/rsa_keys/private.pem", "wb") as f:
        f.write(private_pem)
    
    # Write public key to resource_service
    with open("resource_service/rsa_keys/public.pem", "wb") as f:
        f.write(public_pem)
    
    print("RSA key pair generated successfully!")
    print("Private key: auth_service/rsa_keys/private.pem")
    print("Public key: resource_service/rsa_keys/public.pem")

if __name__ == "__main__":
    generate_rsa_keypair()
