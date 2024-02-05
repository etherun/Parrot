import grpc
import parrot_pb2
import parrot_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = parrot_pb2_grpc.WhisperServiceStub(channel)

def run():
    response = stub.Transcribe(parrot_pb2.AudioPathRequest(path="/home/jaden/Downloads/sample1.flac"))
    print("Text:", response.text)


if __name__ == '__main__':
    run()