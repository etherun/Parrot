import asyncio
import grpc
import parrot_pb2
import parrot_pb2_grpc
from concurrent import futures
import whisper

whisper_model_tiny = whisper.load_model("tiny")


class WhisperServicer(parrot_pb2_grpc.WhisperServiceServicer):
    def Transcribe(self, request, context):
        result = whisper_model_tiny.transcribe(request.path)
        return parrot_pb2.TextResponse(text=result["text"])


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    parrot_pb2_grpc.add_WhisperServiceServicer_to_server(WhisperServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        print("Whisper service terminated.")
