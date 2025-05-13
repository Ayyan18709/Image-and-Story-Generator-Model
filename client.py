import grpc
import texttoimg_pb2
import texttoimg_pb2_grpc
import base64
from PIL import Image
from io import BytesIO

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = texttoimg_pb2_grpc.Text2ImageServiceStub(channel)

        prompt = "a fantasy castle floating in the sky"
        response = stub.GenerateImage(texttoimg_pb2.ImageRequest(prompt=prompt))

        print("Status:", response.status)
        print("Message:", response.message)

        if response.status == "200":
            image_data = base64.b64decode(response.image_base64)
            img = Image.open(BytesIO(image_data))
            img.show()

if __name__ == "__main__":
    run()
