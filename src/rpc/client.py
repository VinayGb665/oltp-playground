import grpc
import src.rpc.proto.unary_pb2 as pb2
import src.rpc.proto.unary_pb2_grpc as pb2_grpc


class UnaryClient:
    def __init__(self, *args, **kwargs):
        self.host = "localhost"
        self.port = 50051
        print(
            "Establishing connection to grpc server at {}:{}".format(
                self.host, self.port
            )
        )
        self.channel = grpc.insecure_channel("{}:{}".format(self.host, self.port))
        self.stub = pb2_grpc.UnaryStub(self.channel)

    def send_req(self, req):
        message = pb2.MessageResponse(message=req)
        return self.stub.GetServerResponse(message)


if __name__ == "__main__":
    client = UnaryClient()
    resp = client.send_req("En Bro Henge")
    print(resp)
