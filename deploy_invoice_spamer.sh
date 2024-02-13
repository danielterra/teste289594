#!/bin/bash

# Load environment variables
source ./.env

# Now you can use the variables in your script
echo "Project ID: $GOOGLE_PROJECT_ID"
echo "Region: $GOOGLE_REGION"

# Exit immediately if a command exits with a non-zero status.
set -e

echo -e "\n\n\n\n=============== START UNIT TESTS ==============="
pytest

# Step 1: Build the Docker image with buildx for the amd64 platform
echo -e "\n\n\n\n=============== BUILD DOCKER IMAGE ==============="
docker buildx build --platform linux/amd64 -f ./Dockerfile.invoice_spamer -t invoice-spamer:amd64 . --load

# Step 2: Tag the Docker image to set the upstream for Google Container Registry
echo -e "\n\n\n\n=============== TAG DOCKER IMAGE ==============="
docker tag invoice-spamer:amd64 ${GOOGLE_REGION}-docker.pkg.dev/${GOOGLE_PROJECT_ID}/${GOOGLE_PROJECT_ID}-docker/invoice-spamer:amd64

# Step 3: Push the Docker image to Google Cloud Artifact Registry
echo -e "\n\n\n\n=============== PUSH IMAGE TO GC ARTIFACT REPO ==============="
docker push ${GOOGLE_REGION}-docker.pkg.dev/${GOOGLE_PROJECT_ID}/${GOOGLE_PROJECT_ID}-docker/invoice-spamer:amd64

# Step 4: Deploy the container as a Cloud Run Job
echo -e "\n\n\n\n=============== DEPLOY GC RUN JOB ==============="
gcloud run jobs deploy invoice-spamer \
    --image ${GOOGLE_REGION}-docker.pkg.dev/${GOOGLE_PROJECT_ID}/${GOOGLE_PROJECT_ID}-docker/invoice-spamer:amd64 \
    --tasks 1 \
    --max-retries 3 \
    --region ${GOOGLE_REGION} \
    --project=${GOOGLE_PROJECT_ID}

echo -e "\n\n\n\n=============== END ==============="
echo "Deployment completed successfully."
