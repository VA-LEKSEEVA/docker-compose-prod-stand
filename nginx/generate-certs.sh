#!/bin/bash
set -e

CERT_DIR="$(dirname "$0")/certs"
mkdir -p "$CERT_DIR"

if [ -f "$CERT_DIR/self-signed.crt" ] && [ -f "$CERT_DIR/self-signed.key" ]; then
    echo "✅ Certificates already exist. Skipping."
    exit 0
fi

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "$CERT_DIR/self-signed.key" \
  -out "$CERT_DIR/self-signed.crt" \
  -subj "/C=RU/ST=Moscow/L=Moscow/O=DevOps/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

echo "✅ Self-signed certificates generated in $CERT_DIR"