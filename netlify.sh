#!/bin/bash

# Stop on error
set -e

# Variables
QUARTO_VERSION="1.7.32"
QUARTO_DL_URL="https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz"
QUARTO_DIR="$HOME/quarto"

# Install Quarto
echo "Installing Quarto v${QUARTO_VERSION}..."
mkdir -p ${QUARTO_DIR}
curl -L "${QUARTO_DL_URL}" -o quarto.tar.gz
tar -zxvf quarto.tar.gz -C ${QUARTO_DIR} --strip-components=1
rm quarto.tar.gz

# Add Quarto to PATH
export PATH=${QUARTO_DIR}/bin:${PATH}

# Verify Quarto installation
echo "Quarto version:"
quarto --version

# Install TinyTeX
echo "Installing TinyTeX..."
quarto install tinytex

# Render the site
echo "Rendering site..."
quarto render

echo "Build finished successfully!"
