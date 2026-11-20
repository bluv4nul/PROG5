import grpc

import library_server
from library.v1 import library_service_pb2, library_service_pb2_grpc, library_pb2

port = 50154
server = library_server.serve(port=port)
try:
    with grpc.insecure_channel(f'127.0.0.1:{port}') as channel:
        stub = library_service_pb2_grpc.LibraryServiceStub(channel)
        book = stub.GetBook(library_service_pb2.GetBookRequest(id=1), timeout=2)
        print(book.title)
        books = stub.AddBooks(iter([library_pb2.Book(id=5, title="The Martian", genre=library_pb2.GENRE_SCIENCE)]), timeout=2)
        print(books.total_books)
finally:
    server.stop(grace=0).wait()
