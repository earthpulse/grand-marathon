FROM oven/bun:1

WORKDIR /app

# Copy package files
COPY package.json bun.lock* ./

# Install dependencies
RUN bun install

# Copy the rest of the application code
COPY . . 

# Expose port 5173
EXPOSE 5173

# Build the SvelteKit project
RUN bun run build

# Run SvelteKit preview server on port 5173 and bind to all interfaces
CMD ["bun", "run", "preview", "--host", "0.0.0.0", "--port", "5173"]
