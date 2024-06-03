from dotenv import load_dotenv
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures, ImageAnalysisResult
from azure.core.credentials import AzureKeyCredential

from PIL import Image

def get_image_data(image_file: str) -> str:
    with open(image_file, "rb") as f:
        image_data = f.read()

def display_image(image_file: str):
    image = Image.open(image_file)
    image.show()

def analyze_image(image_data: bytes) -> ImageAnalysisResult:
    load_dotenv()
    ai_endpoint = os.getenv("AI_SERVICE_ENDPOINT")
    ai_key = os.getenv("AI_SERVICE_KEY")

    # Authenticate Azure AI Vision client
    cv_client = ImageAnalysisClient(
        endpoint=ai_endpoint, credential=AzureKeyCredential(ai_key)
    )

    # Get result with specified features to be retrieved
    result = cv_client.analyze(
        image_data=image_data,
        visual_features=[
            VisualFeatures.CAPTION,
            VisualFeatures.DENSE_CAPTIONS,
            VisualFeatures.TAGS,
            VisualFeatures.OBJECTS,
            VisualFeatures.PEOPLE,
        ],
    )

    # Display analysis results
    # Get image captions
    if result.caption is not None:
        print("\nCaption:")
        print(
            f"Caption: {result.caption.text} (confidence: {100 * result.caption.confidence:.2f}% )"
        )

    # Get image dense captions
    if result.dense_captions is not None:
        print("\nDense Captions:")
        for caption in result.dense_captions.list:
            print(
                f"Caption: {caption.text} (confidence: {100 * caption.confidence:.2f})"
            )

    # Get image tags
    if result.tags is not None:
        print("\nTags:")
        for tag in result.tags.list:
            print(f"Tag: {tag.name}  (confidence: {100 * tag.confidence:.2f})")

    # Get objects in the image
    if result.objects is not None:
        print("\nObjects:")
        for obj in result.objects.list:
            for obj_tag in obj.tags:
                print(
                    f"Object: {obj_tag.name}  (confidence: {100 * obj_tag.confidence:.2f})"
                )

    # Get people in the image
    if result.people is not None:
        print("\nPeople:")
        for person in result.people.list:
            print(f"Tag: {person}  (confidence: {100 * person.confidence:.2f})")
            
    return result


def main():
    image_dir = "images"
    image_file = f"{image_dir}/street.jpg"
    display_image(image_file)

    result: ImageAnalysisResult = analyze_image(image_data=get_image_data(image_file))


if __name__ == "__main__":
    main()
