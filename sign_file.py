from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def sign_file(private_key_path, file_path, output_signature_path):
    with open(private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read())
    with open(file_path, 'rb') as f:
        data = f.read()

    h = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(h)
    with open(output_signature_path, 'wb') as f:
        f.write(signature)
    print(f"Signature saved to {output_signature_path}")

# Example usage:
# sign_file('keys/private_20251024120000.pem', 'contoh.pdf', 'contoh.pdf.sig')
