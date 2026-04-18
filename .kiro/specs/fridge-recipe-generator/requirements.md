# Requirements Document

## Introduction

The Fridge Recipe Generator is a web application that allows users to take or upload a photo of their fridge, automatically detect the ingredients visible in the image using AWS Rekognition, and generate a recipe based on those ingredients. The app is designed to be simple and beginner-friendly, leveraging AWS services (S3, Rekognition, Lambda, API Gateway) for the backend processing.

## Requirements

### Requirement 1: Image Upload

**User Story:** As a user, I want to upload or take a photo of my fridge, so that the app can analyze what ingredients I have.

#### Acceptance Criteria

1. WHEN the user opens the app THEN the system SHALL display an option to upload an image from their device.
2. WHEN the user selects an image file THEN the system SHALL accept JPEG and PNG formats.
3. WHEN the user submits the image THEN the system SHALL upload it to Amazon S3.
4. IF the file is not a supported format THEN the system SHALL display an error message to the user.
5. IF the file exceeds 10MB THEN the system SHALL reject the upload and notify the user.

### Requirement 2: Ingredient Detection

**User Story:** As a user, I want the app to automatically identify ingredients in my fridge photo, so that I don't have to manually list them.

#### Acceptance Criteria

1. WHEN an image is uploaded to S3 THEN the system SHALL trigger an AWS Lambda function to analyze the image.
2. WHEN the Lambda function runs THEN the system SHALL use Amazon Rekognition to detect labels (objects/food items) in the image.
3. WHEN Rekognition returns results THEN the system SHALL filter labels to only include food-related items with a confidence score above 70%.
4. IF no food-related items are detected THEN the system SHALL inform the user and prompt them to try a clearer photo.
5. WHEN ingredients are detected THEN the system SHALL return a list of identified ingredients to the frontend.

### Requirement 3: Recipe Generation

**User Story:** As a user, I want to receive a recipe based on the detected ingredients, so that I know what I can cook with what I have.

#### Acceptance Criteria

1. WHEN ingredients are identified THEN the system SHALL match them against a pre-written recipe library stored in the backend.
2. WHEN matching recipes THEN the system SHALL return the recipe with the highest number of matching ingredients.
3. WHEN a recipe is matched THEN the system SHALL include a recipe name, list of required ingredients, and step-by-step instructions.
4. IF no recipe matches any detected ingredients THEN the system SHALL return a default fallback recipe or a "no match found" message.
5. WHEN the recipe is ready THEN the system SHALL return it to the frontend for display.

### Requirement 4: Results Display

**User Story:** As a user, I want to see the detected ingredients and the generated recipe clearly on the screen, so that I can follow along easily.

#### Acceptance Criteria

1. WHEN the analysis is complete THEN the system SHALL display the list of detected ingredients on the page.
2. WHEN a recipe is returned THEN the system SHALL display the recipe name, ingredients, and instructions in a readable format.
3. WHEN the app is processing the image THEN the system SHALL show a loading indicator so the user knows something is happening.
4. IF an error occurs at any stage THEN the system SHALL display a user-friendly error message.

### Requirement 5: API Communication

**User Story:** As a developer, I want the frontend to communicate with the backend through a well-defined API, so that the system is modular and easy to maintain.

#### Acceptance Criteria

1. WHEN the frontend submits an image THEN the system SHALL send it to an Amazon API Gateway endpoint.
2. WHEN API Gateway receives a request THEN the system SHALL route it to the appropriate AWS Lambda function.
3. WHEN the Lambda function completes THEN the system SHALL return a JSON response containing ingredients and recipe data.
4. IF the Lambda function fails THEN the system SHALL return an appropriate HTTP error code and message.
