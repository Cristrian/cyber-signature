"""Service in charge of signing and verifying signatures.

This service is a wrapper around the cryptography library. It provides
a simple interface for signing and verifying signatures.
"""
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


def generate_keypair() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    """Generate a new keypair.

    Returns:
        The private key.
        The public key.
    """
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    return private_key, public_key


def sign(
    message: bytes, private_key: Ed25519PrivateKey | None = None
) -> tuple[bytes, Ed25519PrivateKey]:
    """Sign a message.

    Args:
        message: The message to sign.
        private_key: The private key to use for signing. If not provided,
            a new key will be generated.

    Returns:
        The signature.
        The private key used for signing.
    """
    if private_key is None:
        private_key = Ed25519PrivateKey.generate()

    return private_key.sign(message), private_key


def verify(message: bytes, signature: bytes, public_key: Ed25519PublicKey) -> bool:
    """Verify a signature.

    Args:
        message: The message to verify.
        signature: The signature to verify.
        public_key: The public key to use for verification.

    Returns:
        True if the signature is valid, False otherwise.
    """
    try:
        public_key.verify(signature, message)
        return True
    except InvalidSignature:
        return False
