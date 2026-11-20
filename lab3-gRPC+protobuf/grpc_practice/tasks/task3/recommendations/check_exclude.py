import grpc
from recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub

with grpc.insecure_channel("127.0.0.1:50153") as channel:
    response = RecommendationsStub(channel).Recommend(
        RecommendationRequest(
            user_id=1,
            category=BookCategory.BOOK_CATEGORY_SCIENCE_FICTION,
            max_results=10,
            exclude_ids=[5],
        ),
        timeout=5,
    )

ids = sorted(book.id for book in response.recommendations)
print(ids)
assert ids == [6, 7, 8], ids
