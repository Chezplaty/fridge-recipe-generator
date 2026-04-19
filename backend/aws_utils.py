import boto3

rekognition = boto3.client("rekognition", region_name="us-west-2")

def detect_ingredients(image_bytes):
    
    response = rekognition.detect_labels(
                Image={"Bytes": image_bytes},
                MaxLabels=10,
                MinConfidence=70
    )

    labels = [label["Name"].lower() for label in response["Labels"]]

    return labels