const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const path = require("path");

const PROTO_PATH = path.join(__dirname, "../protos/ai_inference.proto");

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const proto = grpc.loadPackageDefinition(packageDefinition).aiinference;

const client = new proto.AIInference(
  "localhost:8080",
  grpc.credentials.createInsecure()
);

const metadata = new grpc.Metadata();
metadata.add("authorization", "Bearer my-secret-key");

function testUnary() {
  return new Promise((resolve) => {
    console.log("\n========== Task 2: Unary RPC - Sentiment Analysis ==========");

    const deadline = new Date();
    deadline.setSeconds(deadline.getSeconds() + 2);

    client.AnalyzeSentiment(
      {
        text: "I love this product. It is amazing and excellent!"
      },
      metadata,
      {
        deadline
      },
      (error, response) => {
        if (error) {
          if (error.code === grpc.status.DEADLINE_EXCEEDED) {
            console.log("Friendly message: Sentiment request timed out after 2 seconds.");
          } else {
            console.log(`gRPC Error: ${error.message}`);
          }

          resolve();
          return;
        }

        console.log("Sentiment Label:", response.label);
        console.log("Confidence:", response.confidence);

        resolve();
      }
    );
  });
}

function testServerStreaming() {
  return new Promise((resolve) => {
    console.log("\n========== Task 3: Server Streaming - Text Generation ==========");

    const call = client.GenerateText(
      {
        prompt: "Explain why gRPC is useful for AI services"
      },
      metadata
    );

    process.stdout.write("AI Response: ");

    call.on("data", (chunk) => {
      process.stdout.write(chunk.token);
    });

    call.on("end", () => {
      console.log();
      resolve();
    });

    call.on("error", (error) => {
      console.log(`gRPC Error: ${error.message}`);
      resolve();
    });
  });
}

function testClientStreaming() {
  return new Promise((resolve) => {
    console.log("\n========== Task 4: Client Streaming - Batch Summarization ==========");

    const call = client.SummarizeDocument(metadata, (error, response) => {
      if (error) {
        console.log(`gRPC Error: ${error.message}`);
        resolve();
        return;
      }

      console.log("Summary:", response.summary);
      resolve();
    });

    const chunks = [
      "gRPC is a high-performance RPC framework. ",
      "It uses HTTP/2 and Protocol Buffers. ",
      "It supports unary, server streaming, client streaming, and bidirectional streaming. ",
      "This makes it useful for AI systems that need low latency and streaming output."
    ];

    chunks.forEach((chunk, index) => {
      console.log(`Sending chunk ${index + 1}: ${chunk}`);
      call.write({
        content: chunk
      });
    });

    call.end();
  });
}

function testBidirectionalStreaming() {
  return new Promise((resolve) => {
    console.log("\n========== Task 5: Bidirectional Streaming - Live Chat ==========");

    const call = client.LiveChat(metadata);

    call.on("data", (message) => {
      console.log(`${message.role}: ${message.content}`);
    });

    call.on("end", () => {
      resolve();
    });

    call.on("error", (error) => {
      console.log(`gRPC Error: ${error.message}`);
      resolve();
    });

    const messages = [
      "Hello assistant.",
      "What is gRPC?",
      "Why is streaming useful for LLMs?"
    ];

    messages.forEach((msg, index) => {
      setTimeout(() => {
        console.log(`user: ${msg}`);

        call.write({
          role: "user",
          content: msg
        });

        if (index === messages.length - 1) {
          setTimeout(() => {
            call.end();
          }, 1000);
        }
      }, index * 1000);
    });
  });
}

async function main() {
  await testUnary();
  await testServerStreaming();
  await testClientStreaming();
  await testBidirectionalStreaming();
}

main();