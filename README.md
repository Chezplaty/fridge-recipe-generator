# Fridge Recipe Generator

A serverless web app that scans a photo of your fridge and suggests a recipe based on the ingredients it detects. Upload a picture, and the app uses AI-powered image recognition to identify what's inside and match it to a real recipe.

---

## Demo

[![Demo Video](https://img.youtube.com/vi/nEkEr5j_36w/0.jpg)](https://www.youtube.com/watch?v=nEkEr5j_36w)

---

## How It Works

1. User uploads a photo of their fridge through the web interface
2. The image is sent to an AWS Lambda function as a base64-encoded payload
3. AWS Rekognition analyzes the image and detects food labels (70%+ confidence)
4. The detected ingredients are matched against TheMealDB recipe database
5. The best-matching recipe (most ingredient overlap) is returned and displayed

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, Vanilla JS, CSS3 |
| Backend | Python 3, AWS Lambda |
| Image Recognition | AWS Rekognition |
| Recipe Data | [TheMealDB API](https://www.themealdb.com/api.php) |
| API Gateway | AWS API Gateway (REST, CORS-enabled) |
| Storage | AWS S3 (image upload) |

---

## Project Structure

```
fridge-recipe-generator/
├── backend/
│   ├── app.py          # Lambda handler entry point
│   ├── aws_utils.py    # Rekognition & S3 integrations
│   ├── recipes.py      # Recipe matching logic
│   ├── requirements.txt
│   └── function.zip    # Ready-to-deploy Lambda package
└── frontend/
    ├── index.html      # Single-page app
    ├── script.js       # Image upload, API calls, result rendering
    ├── style.css       # UI styling
    └── mascot.png      # App mascot image
```

---

## Prerequisites

- An AWS account with permissions to use Lambda, API Gateway, Rekognition, and S3
- A configured Lambda IAM execution role with:
  - `s3:PutObject`
  - `rekognition:DetectLabels`

---

## Deployment

### Backend (AWS Lambda)

1. Create an AWS Lambda function with a **Python 3.11+** runtime.
2. Upload `backend/function.zip` as the deployment package.
3. Set the handler to `app.lambda_handler`.
4. Attach an IAM role with the permissions listed above.
5. Create an API Gateway **POST** endpoint and link it to the Lambda function.
6. Enable **CORS** on the API Gateway resource.

### Frontend

1. Copy the contents of the `frontend/` directory to any static hosting (S3 + CloudFront, GitHub Pages, Netlify, etc.).
2. Open `frontend/script.js` and update the `API_URL` constant to your API Gateway endpoint:

```javascript
const API_URL = "https://<your-api-id>.execute-api.<region>.amazonaws.com/recipe";
```

3. Open `frontend/index.html` in a browser.

---

## Configuration

| Setting | Location | Default | Description |
|---|---|---|---|
| `API_URL` | `frontend/script.js` | AWS API Gateway URL | Lambda endpoint |
| AWS Region | `backend/aws_utils.py` | `us-west-2` | Rekognition service region |
| Rekognition confidence | `backend/aws_utils.py` | `70%` | Minimum confidence for label detection |
| Max Rekognition labels | `backend/aws_utils.py` | `10` | Max labels returned per image |

AWS credentials are provided automatically via the Lambda execution role — no keys need to be hardcoded.

---

## Local Development

The backend requires an active AWS account and cannot be run fully offline. For frontend-only development:

```bash
# Open the frontend directly in a browser
open frontend/index.html
```

Make sure the `API_URL` in `script.js` points to a deployed and CORS-enabled API Gateway endpoint.

To rebuild the Lambda deployment package after modifying backend code:

```bash
cd backend
pip install -r requirements.txt -t .
zip -r function.zip .
```

---

## API Reference

**POST** `/recipe`

**Request body:**
```json
{
  "image": "<base64-encoded image string>"
}
```

**Response:**
```json
{
  "labels": ["chicken", "tomato", "onion"],
  "recipe": {
    "name": "Chicken Cacciatore",
    "ingredients": ["chicken", "tomato", "onion", "garlic", "olive oil"],
    "instructions": "...",
    "thumbnail": "https://www.themealdb.com/images/media/meals/..."
  }
}
```

If no matching recipe is found, the `recipe` field will contain a fallback message.

---

## Built With

- [AWS Rekognition](https://aws.amazon.com/rekognition/) — image label detection
- [AWS Lambda](https://aws.amazon.com/lambda/) — serverless compute
- [AWS API Gateway](https://aws.amazon.com/api-gateway/) — REST API
- [TheMealDB](https://www.themealdb.com/) — free recipe database
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) — AWS SDK for Python
