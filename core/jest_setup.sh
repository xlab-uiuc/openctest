#!/bin/bash

echo "Installing Node.js and npm..."
sudo apt update
sudo apt install -y nodejs npm

echo "Node.js and npm installed:"
node --version
npm --version

echo "Installing Jest..."
npm install --global jest

echo "Jest installed:"
jest --version

echo "Environment setup complete. You can now use Jest for testing."