import json
import os
from PIL import Image
import piexif
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

def generate_key_pair():
    """Generates a new Ed25519 key pair for signing."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

def sign_data(private_key, data: bytes) -> bytes:
    """Signs arbitrary binary data using the private key."""
    return private_key.sign(data)

def embed_signature_in_image(image_path: str, output_path: str, creator_name: str, private_key):
    """
    Reads an image, signs its raw pixel data alongside metadata,
    and writes the signature and creator info into the EXIF UserComment field.
    """
    img = Image.open(image_path)
    
    # Extract raw image bytes for hashing/signing
    image_bytes = img.tobytes()
    
    # Construct the metadata payload
    payload = {
        "creator": creator_name,
        "protected": True
    }
    payload_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
    
    # Create signature over the combined image content and payload
    signature = sign_data(private_key, image_bytes + payload_bytes)
    
    # Store payload and signature (hex-encoded) in a structured dictionary
    provenance_data = {
        "payload": payload,
        "signature_hex": signature.hex()
    }
    
    metadata_json = json.dumps(provenance_data)
    
    # Load existing EXIF data or create a blank structure
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    if "exif" in img.info:
        try:
            exif_dict = piexif.load(img.info["exif"])
        except Exception:
            pass
            
    # Embed metadata into EXIF tag 37510 (UserComment)
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = metadata_json.encode('utf-8')
    exif_bytes = piexif.dump(exif_dict)
    
    # Save the new signed image
    img.save(output_path, exif=exif_bytes)
