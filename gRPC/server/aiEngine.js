function analyzeSentiment(text) {
  const lower = text.toLowerCase();

  const positiveWords = ["good", "great", "excellent", "love", "amazing", "best", "happy"];
  const negativeWords = ["bad", "terrible", "hate", "worst", "poor", "awful", "sad"];

  const positiveScore = positiveWords.filter((word) => lower.includes(word)).length;
  const negativeScore = negativeWords.filter((word) => lower.includes(word)).length;

  if (positiveScore > negativeScore) {
    return { label: "POSITIVE", confidence: 0.92 };
  }

  if (negativeScore > positiveScore) {
    return { label: "NEGATIVE", confidence: 0.9 };
  }

  return { label: "NEUTRAL", confidence: 0.7 };
}

function generateText(prompt) {
  return `This is a simulated AI response for: "${prompt}". The server is streaming this response token by token using gRPC server streaming.`;
}

function summarizeText(text) {
  const words = text.split(/\s+/);

  if (words.length <= 30) {
    return `Short summary: ${text}`;
  }

  return `Summary: The document mainly discusses ${words.slice(0, 25).join(" ")}...`;
}

function chatResponse(message, history) {
  return `I received your message: "${message}". This conversation now has ${history.length} message(s).`;
}

module.exports = {
  analyzeSentiment,
  generateText,
  summarizeText,
  chatResponse
};