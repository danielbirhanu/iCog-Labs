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

const PORT = 50051;
const API_KEY = "my-secret-key";

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
  // Bonus deadline test: client timeout is 2s, server sleeps 3s
  setTimeout(() => {
    const result = analyzeSentiment(call.request.text);

    callback(null, {
      label: result.label,
      confidence: result.confidence
    });
  }, 3000);
}

function GenerateText(call) {
  if (!checkAuth(call)) return;

  const response = generateText(call.request.prompt);
  const tokens = response.split(" ");

  let index = 0;

  const interval = setInterval(() => {
    if (index >= tokens.length) {
      clearInterval(interval);
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

  console.log(`[Server ${PORT}] Client streaming started`);

  let fullText = "";

  call.on("data", (chunk) => {
    console.log(`[Server ${PORT}] Received chunk: ${chunk.content.substring(0, 40)}...`);
    fullText += chunk.content + " ";
  });

  call.on("end", () => {
    const summary = summarizeText(fullText);

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

  console.log(`[Server ${PORT}] Bidirectional streaming chat started`);

  const history = [];

  call.on("data", (message) => {
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
    call.end();
  });

  call.on("error", (err) => {
    console.error("Live chat error:", err.message);
  });
}

function main() {
  const server = new grpc.Server();

  server.addService(proto.AIInference.service, {
    AnalyzeSentiment,
    GenerateText,
    SummarizeDocument,
    LiveChat
  });

  server.bindAsync(
    `0.0.0.0:${PORT}`,
    grpc.ServerCredentials.createInsecure(),
    (error, bindPort) => {
      if (error) {
        console.error(error);
        return;
      }

      console.log(`gRPC AI Inference Server running on port ${bindPort}`);
      server.start();
    }
  );
}

main();