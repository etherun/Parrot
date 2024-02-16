import asyncio
import json
import grpc
import parrot_pb2
import parrot_pb2_grpc
from concurrent import futures
import whisper
from transformers import pipeline

whisper_model_tiny = whisper.load_model("tiny")
sentiment_classifier = pipeline(
    "text-classification",
    model="/home/jaden/.cache/huggingface/hub/models--j-hartmann--emotion-english-distilroberta-base",
    return_all_scores=True
)


class WhisperServicer(parrot_pb2_grpc.WhisperServiceServicer):
    def Transcribe(self, request, context):
        result = whisper_model_tiny.transcribe(request.path)
        return parrot_pb2.TextResponse(text=result["text"])


class EmotionServicer(parrot_pb2_grpc.TextSentimentAnalysisServicer):
    def Predict(self, request, context):
        result = sentiment_classifier(request.text)
        return parrot_pb2.TextResponse(text=json.dumps(result[0]))


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    parrot_pb2_grpc.add_WhisperServiceServicer_to_server(WhisperServicer(), server)
    parrot_pb2_grpc.add_TextSentimentAnalysisServicer_to_server(EmotionServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        print("Whisper service terminated.")
