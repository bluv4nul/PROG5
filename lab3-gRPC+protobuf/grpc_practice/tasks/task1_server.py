"""Сервер gRPC: реализация сервиса task1.Greeter."""
import logging
from concurrent import futures

import grpc
import task1_pb2
import task1_pb2_grpc


class Greeter(task1_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return task1_pb2.HelloReply(message=f"Hello, {request.name}!")

    def SayHelloAgain(self, request, context):
        return task1_pb2.HelloReply(message=f"Hello again, {request.name}!")

    def SayGoodbye(self, request, context):
        return task1_pb2.GoodbyeReply(message=f"Goodbye, {request.name}!")


def serve() -> tuple[grpc.Server, int]:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task1_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    port = server.add_insecure_port('127.0.0.1:0')
    server.start()
    return server, port
