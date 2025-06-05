#!/bin/bash
set -e

apt-get update

# Install common development utilities
apt-get install -y --no-install-recommends \
    procps \
    iputils-ping \
    curl \
    wget \
    netcat-openbsd \
    iproute2 \
    net-tools \
    lsof \
    htop \
    gnupg \
    git \
    lsb-release \
    ssh \
    ca-certificates

update-ca-certificates

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor --yes -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the stable repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index again
apt-get update

# Install Docker CLI only
apt-get install -y docker-ce-cli

git config --global --add safe.directory /app
