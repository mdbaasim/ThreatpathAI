#!/usr/bin/env bash
# Exit on any error
set -o errexit

echo "==> 1. Building React Frontend..."
cd threatpath/frontend-app
npm install
npm run build

echo "==> 2. Installing Python Backend Dependencies..."
cd ../backend
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Build Completed Successfully!"
