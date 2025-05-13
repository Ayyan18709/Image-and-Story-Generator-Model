import grpc
from concurrent import futures
import texttoimg_pb2
import texttoimg_pb2_grpc
from image_generator import StoryImageGenerator

class StoryImageGeneratorServiceServicer(texttoimg_pb2_grpc.StoryImageGeneratorServiceServicer):
    def __init__(self):
        self.generator = StoryImageGenerator()

    def GenerateStoryAndImages(self, request, context):
            story, images_base64 = self.generator.generate_story_and_images(request.prompt)
            return texttoimg_pb2.StoryImageResponse(
                story=story,
                images_base64=images_base64)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    texttoimg_pb2_grpc.add_StoryImageGeneratorServiceServicer_to_server(
        StoryImageGeneratorServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("✅ gRPC server is running on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
