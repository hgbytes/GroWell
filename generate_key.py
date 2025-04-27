import secrets
import base64

def generate_secret_key():
    # Generate a random 32-byte key
    random_bytes = secrets.token_bytes(32)
    # Convert to base64 for better readability
    secret_key = base64.b64encode(random_bytes).decode('utf-8')
    return secret_key

if __name__ == '__main__':
    key = generate_secret_key()
    print("\nGenerated Secret Key:")
    print("=" * 50)
    print(key)
    print("=" * 50)
    print("\nCopy this key and replace 'your_flask_secret_key_here' in your .env file") 