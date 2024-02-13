# Objectives
- Create 8 to 12 invoices per hour for 24 hours
- Capture webhook events for the paid invoices and transfer the funds to the following account

## Funds receiver account
- bank code: 20018183
- branch: 0001
- account: 6341320293482496
- name: Stark Bank S.A.
- tax ID: 20.018.183/0001-80
- account type: payment

# Architecture

## Environment
- Language: Python 3.10.7
- Environment manager: PyEnv
- Unit testing: PyTest
- Cloud Services: Google Cloud
  - Runtime: Cloud Run
  - Cron job Scheduler: Cloud Scheduler
  - Message queue: Cloud Pub/Sub

## Strategy
We are going to use GCP Pub/Sub to safely store and acknowledge each operation done between Stark and the script, if anything goes wrong, we can process those events again as needed within 7 days.

# Proccess
## Sending invoices
1. Cloud Scheduler 
   1. Will schedule the execution of the InvoiceSpamer.py each hour for 24 hours
2. Cloud Run -> InvoiceSpamer
   1. Generate 12 invoices pushing the events into pending_invoices queue.
3. Cloud Pub/Sub -> pending_invoices
   1. POST request to InvoiceSender to fullfil the invoices

## Trasfer funds
4. Cloud Pub/Sub stark_invoice_updates
   1. Will receive a  http call from StarkBank with the invoice new status and push the message to paid_invoices queue and request InvoiceUpdater
5. Cloud Pub/Sub -> paid_invoices
   1. Do a http request for each paid invoice to MoneySender
6. Cloud Run -> MoneySender
   1. Request StarkBank to transfer the funds and aknowledge the message

# Unit testing
- Run `pytest` on the main folder

# Setup
## .env file
```
BASE_URL=https://sandbox.api.starkbank.com
```
## StarkBank keys
1. Run the `python setup.py` script to generate a brand new public and private keys
2. Register the public key with Stark Bank as new Project

## Google Cloud Artifact
1. Create a Google Cloud Artifact Repository for the Docker images
```
gcloud artifacts repositories create teste289594-docker --repository-format=docker \
--location=southamerica-east1 --description="Docker repository"
```
2. Run `gcloud auth configure-docker southamerica-east1-docker.pkg.dev` to set as default artifact repo

# Deploy
1. Install Google Cloud CLI and configure with the project
***Im running on a Mac in a arm architecture, we need to use buildx to target linux/amd64 to be used in GC***
2. Run `docker buildx create --name teste289594 --use` to setup the docker builder
3. Run `docker buildx inspect --bootstrap` to init buildx

## Deploy invoice_spammer JOB
1. Run `docker buildx build --platform linux/amd64 -f ./Dockerfile.invoice_spamer -t invoice-spamer:amd64 . --load` to create the docker image
2. Set the docker file upstream
```
docker tag invoice-spamer:amd64 \
southamerica-east1-docker.pkg.dev/teste289594/teste289594-docker/invoice-spamer:amd64
```
1. Run `docker push southamerica-east1-docker.pkg.dev/teste289594/teste289594-docker/invoice-spamer:amd64`
2. Run the command to deploy as a Cloud Run Job, the container will be created automatically and pass the environment variables
```
gcloud run jobs deploy invoice-spamer \
    --image southamerica-east1-docker.pkg.dev/teste289594/teste289594-docker/invoice-spamer:amd64 \
    --tasks 1 \
    --max-retries 3 \
    --region southamerica-east1 \
    --project=teste289594
```

## Deploy invoice_updater service
