#!/bin/bash

# This creates the hidden file Kestra needs
# It takes the GitHub Secret and turns it into the Base64 format
echo "SECRET_GCP_CREDS=$(echo -n "$GCP_SERVICE_ACCOUNT_JSON" | base64 -w 0)" > .env_encoded

echo ".env_encoded has been created successfully!"