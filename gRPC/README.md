# AI Inference gRPC Demo

This project is a small Node.js gRPC demo that simulates an AI inference service. It shows how a client can call a backend service using different gRPC communication patterns: unary calls, server streaming, client streaming, and bidirectional streaming.

The system uses Nginx as a gRPC load balancer in front of three identical backend server containers.

## Workflow

The client sends gRPC requests to Nginx on `localhost:8080`. Nginx forwards each request to one of the backend Node.js gRPC servers. The server checks the API key from the request metadata, handles the RPC method, calls the mock AI logic in `server/aiEngine.js`, and sends the response back to the client.

```txt
client/client.js
      |
      | gRPC request
      v
Nginx load balancer :8080
      |
      v
server1 / server2 / server3 :50051
      |
      v
server/aiEngine.js
```

## Project Structure

```txt
gRPC/
  client/
    client.js          # Test client for all RPC methods
    package.json       # Client dependencies and start script

  server/
    server.js          # gRPC server implementation
    aiEngine.js        # Mock AI logic
    Dockerfile         # Server Docker image
    package.json       # Server dependencies and start script

  protos/
    ai_inference.proto # Shared gRPC service contract

  nginx/
    nginx.conf         # gRPC load balancer configuration

  docker-compose.yml   # Runs 3 servers and Nginx
  README.md
```

## RPC Methods

The service is defined in `protos/ai_inference.proto`.

### 1. Unary RPC: Sentiment Analysis

The client sends one text request and receives one sentiment response.

```txt
AnalyzeSentiment(SentimentRequest) -> SentimentResponse
```

This method also demonstrates gRPC deadlines. The client waits 2 seconds, while the server intentionally responds after 3 seconds, so the request should time out.

### 2. Server Streaming: Text Generation

The client sends one prompt, and the server streams the response back token by token.

```txt
GenerateText(GenerationRequest) -> stream GenerationChunk
```

This is similar to how AI chat apps stream generated text.

### 3. Client Streaming: Document Summarization

The client sends several document chunks, and the server returns one summary after the client finishes streaming.

```txt
SummarizeDocument(stream DocumentChunk) -> SummaryResponse
```

### 4. Bidirectional Streaming: Live Chat

The client and server both send messages over the same open stream.

```txt
LiveChat(stream ChatMessage) -> stream ChatMessage
```

This demonstrates a live conversation-style connection.

## Authentication

Every request must include this metadata:

```txt
authorization: Bearer my-secret-key
```

The server compares the token against the `API_KEY` environment variable. If no environment variable is provided, it uses:

```txt
my-secret-key
```

## Run With Docker

From the `gRPC` directory:

```powershell
docker compose up --build
```

This starts:

- `server1`
- `server2`
- `server3`
- `nginx`

Nginx listens on:

```txt
localhost:8080
```

Each backend server listens internally on:

```txt
50051
```

## Run The Client

Open another terminal and run:

```powershell
cd client
npm install
npm start
```

The client will run all four RPC demos in order.

## Expected Behavior

You should see output for:

- Unary sentiment analysis timeout
- Server-streamed generated text
- Client-streamed document summarization
- Bidirectional live chat messages

The unary request is expected to timeout because the client deadline is shorter than the server delay.

## Main Files

- `protos/ai_inference.proto`: defines the service, RPC methods, and message types.
- `server/server.js`: creates the gRPC server and implements the RPC handlers.
- `server/aiEngine.js`: contains mock AI functions used by the server.
- `client/client.js`: calls all service methods and prints the responses.
- `nginx/nginx.conf`: load balances gRPC requests across server containers.
- `docker-compose.yml`: starts the full multi-container setup.

## Notes

This project does not use a real AI model. The AI behavior is simulated so the focus stays on understanding gRPC communication patterns, streaming, metadata authentication, deadlines, Docker, and load balancing.
