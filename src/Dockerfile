# The base image is already Ubuntu, which is great.
FROM docker.io/pandoc/extra:3.7-ubuntu

# Install run-time, compile-time, and dev-time system dependencies using apt-get for Ubuntu
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Install dependencies for adding the NodeSource repository
    ca-certificates \
    curl \
    gnupg \
    # Add NodeSource GPG key and repository for Node.js 20.x
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && NODE_MAJOR=20 \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    # Update apt cache again and install all packages
    # Note: 'npm' is not listed here because it is included with the 'nodejs' package from NodeSource
    && apt-get update && apt-get install -y --no-install-recommends \
    make \
    nodejs \
    inotify-tools \
    bash \
    ripgrep \
    imagemagick \
    # Clean up the apt cache to reduce image size
    && rm -rf /var/lib/apt/lists/*

RUN tlmgr install texfot texlogfilter texlogsieve

# Create a new user 'runner' with UID/GID 1001 to avoid conflicts with the default user.
# The -m flag creates a home directory at /home/runner
RUN groupadd -g 1001 runner \
    && useradd -g runner -u 1001 -m -s /bin/bash runner

# Give the 'runner' user ownership of the global node installation directories.
# The path /usr/lib/node_modules is used by the NodeSource installation on this system.
USER root
RUN mkdir -p /usr/lib/node_modules \
    && chown -R runner:runner /usr/lib/node_modules \
    && chown -R runner:runner /usr/bin

# Switch to the non-root user for subsequent commands
USER runner

# Create required folders and set the working directory in the user's home
RUN mkdir /home/runner/src
WORKDIR /home/runner/src

# Install run-time and compile-time project dependencies
# (No dependencies listed in the original file)

# Install dev-time local dependencies as the non-root user
# This now works because the user owns the global install directories
RUN npm install -g @google/gemini-cli

# Install dev-time project dependencies
# (No dependencies listed in the original file)

# The WORKDIR is already set, so no need to change it again

# Expose required ports
# (No ports listed in the original file)

# Define entrypoint
ENTRYPOINT ["/bin/bash"]

