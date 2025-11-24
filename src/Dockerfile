FROM docker.io/pandoc/extra:3.7-ubuntu

# Install deps
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
    && apt-get update && apt-get install -y --no-install-recommends \
    make \
    nodejs \
    inotify-tools \
    bash \
    ripgrep \
    imagemagick \
    # Not really needed, but I use these for some projects
    build-essential \
    python3-venv \
    libomp-dev \
    # Clean up the apt cache to reduce image size
    && rm -rf /var/lib/apt/lists/* \
    && tlmgr update --self \
    && tlmgr install texfot texlogfilter texlogsieve

RUN groupadd -g 1001 runner \
    && useradd -g runner -u 1001 -m -s /bin/bash runner

RUN mkdir -p /usr/lib/node_modules \
    && chown -R runner:runner /usr/lib/node_modules \
    && chown -R runner:runner /usr/bin

# Switch to the non-root user
USER runner

# Create required folders and set the working directory in the user's home
RUN mkdir /home/runner/src
WORKDIR /home/runner/src

# Install run-time and compile-time project dependencies

# Install dev-time local dependencies as the non-root user
RUN npm install -g @openai/codex \
    && npm install -g @google/gemini-cli@nightly

# Install dev-time project dependencies

# Define entrypoint
ENTRYPOINT ["/bin/bash"]

