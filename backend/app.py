import json
from recipes import find_best_recipe
import aws_utils
import base64

def lambda_handler(event, context):

    body = json.loads(event.get("body", "{}"))
    image_base64 = body.get("image", "")
    image_bytes = base64.b64decode(image_base64)

    ingredients = aws_utils.detect_ingredients(image_bytes)

    recipe = find_best_recipe(ingredients)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "labels": ingredients,
            "recipe": recipe
        })
    }