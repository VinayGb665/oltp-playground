import grpc
from concurrent import futures
import time
import src.rpc.proto.unary_pb2 as pb2
import src.rpc.proto.unary_pb2_grpc as pb2_grpc


class UnaryService(pb2_grpc.UnaryServicer):
    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):
        message = request.message
        result = f"Fo dude why you woke me up"
        result = {"message": result, "count": "2"}
        return pb2.MessageResponse(**result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_UnaryServicer_to_server(UnaryService(), server)
    port = 50051
    server.add_insecure_port(f"[::]:{port}")
    print(f"Starting grpc server at {port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
