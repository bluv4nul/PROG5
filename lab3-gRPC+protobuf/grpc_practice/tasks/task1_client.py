"""Клиент gRPC для сервиса task1.Greeter."""
import grpc
import task1_pb2
import task1_pb2_grpc
import task1_server


def run(port: int) -> None:
    print("Will try to greet world ...")
    # Канал — соединение с сервером; with закрывает его по завершении
    with grpc.insecure_channel(f'127.0.0.1:{port}') as channel:
        stub = task1_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(task1_pb2.HelloRequest(name="you"), timeout=5)
        print("Greeter client received:", response.message)
        response = stub.SayHelloAgain(task1_pb2.HelloRequest(name="you"), timeout=5)
        print("Greeter client received:", response.message)
        response = stub.SayGoodbye(task1_pb2.GoodbyeRequest(name="you"), timeout=5)
        print("Greeter client received:", response.message)


if __name__ == '__main__':
    server, port = task1_server.serve()
    try:
        run(port)
    finally:
        server.stop(grace=0).wait()
