const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const path = require("path");

const {
  analyzeSentiment,
  generateText,
  summarizeText,
  chatResponse
} = require("./aiEngine");

const PROTO_PATH = path.join(__dirname, "../protos/ai_inference.proto");

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const proto = grpc.loadPackageDefinition(packageDefinition).aiinference;

const HOST = process.env.SERVER_HOST || "127.0.0.1";
const PORT = process.env.SERVER_PORT || 50051;
const API_KEY = process.env.API_KEY || "my-secret-key";

function checkAuth(call, callback) {
  const metadata = call.metadata.get("authorization");
  const token = metadata[0];

  if (token !== `Bearer ${API_KEY}`) {
    const error = {
      code: grpc.status.UNAUTHENTICATED,
      message: "Invalid or missing API key"
    };

    if (callback) callback(error);
    else call.emit("error", error);

    return false;
  }

  return true;
}

function AnalyzeSentiment(call, callback) {
  if (!checkAuth(call, callback)) return;

  console.log(`\n[Server ${PORT}] Unary RPC - AnalyzeSentiment`);
  console.log(`[Server ${PORT}] Text: ${call.request.text}`);

  // Bonus deadline test: client timeout is 2s, server sleeps 3s
  setTimeout(() => {
    const result = analyzeSentiment(call.request.text);

    console.log(`[Server ${PORT}] Sentiment result: ${result.label} (${result.confidence})`);

    callback(null, {
      label: result.label,
      confidence: result.confidence
    });
  }, 3000);
}

function GenerateText(call) {
  if (!checkAuth(call)) return;

  console.log(`\n[Server ${PORT}] Server Streaming RPC - GenerateText`);
  console.log(`[Server ${PORT}] Prompt: ${call.request.prompt}`);

  const response = generateText(call.request.prompt);
  const tokens = response.split(" ");

  let index = 0;

  const interval = setInterval(() => {
    if (index >= tokens.length) {
      clearInterval(interval);
      console.log(`[Server ${PORT}] Text generation stream completed`);
      call.end();
      return;
    }

    call.write({
      token: tokens[index] + " "
    });

    index++;
  }, 150);
}

function SummarizeDocument(call, callback) {
  if (!checkAuth(call, callback)) return;

  console.log(`\n[Server ${PORT}] Client Streaming RPC - SummarizeDocument`);
  console.log(`[Server ${PORT}] Client streaming started`);

  let fullText = "";

  call.on("data", (chunk) => {
    console.log(`[Server ${PORT}] Received chunk: ${chunk.content.substring(0, 40)}...`);
    fullText += chunk.content + " ";
  });

  call.on("end", () => {
    const summary = summarizeText(fullText);

    console.log(`[Server ${PORT}] Summary generated`);

    callback(null, {
      summary
    });
  });

  call.on("error", (err) => {
    console.error("Client streaming error:", err.message);
  });
}

function LiveChat(call) {
  if (!checkAuth(call)) return;

  console.log(`\n[Server ${PORT}] Bidirectional Streaming RPC - LiveChat`);
  console.log(`[Server ${PORT}] Bidirectional streaming chat started`);

  const history = [];

  call.on("data", (message) => {
    console.log(`[Server ${PORT}] ${message.role}: ${message.content}`);

    history.push({
      role: message.role,
      content: message.content
    });

    const reply = chatResponse(message.content, history);

    call.write({
      role: "assistant",
      content: reply
    });
  });

  call.on("end", () => {
    console.log(`[Server ${PORT}] Live chat stream ended`);
    call.end();
  });

  call.on("error", (err) => {
    console.error("Live chat error:", err.message);
  });
}

function main() {
  const server = new grpc.Server();
  const keepAlive = setInterval(() => {}, 1 << 30);

  server.addService(proto.AIInference.service, {
    AnalyzeSentiment,
    GenerateText,
    SummarizeDocument,
    LiveChat
  });

  server.bindAsync(
    `${HOST}:${PORT}`,
    grpc.ServerCredentials.createInsecure(),
    (error, bindPort) => {
      if (error) {
        console.error(error);
        return;
      }

      console.log(`gRPC AI Inference Server running on ${HOST}:${bindPort}`);
      server.start();
    }
  );

  process.on("SIGINT", () => {
    clearInterval(keepAlive);
    server.tryShutdown(() => process.exit(0));
  });

  process.on("SIGTERM", () => {
    clearInterval(keepAlive);
    server.tryShutdown(() => process.exit(0));
  });
}

main();
