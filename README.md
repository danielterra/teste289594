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


# Proccess
## Sending invoices
1. Cloud Scheduler 
   1. Will schedule the execution of the invoice_spamer each hour
2. Cloud Run -> invoice_spamer
   1. Generate 8 invoices
## Trasfer funds
1. Cloud Run money_sender
   1. Will receive a  http call from StarkBank with the invoice new status request StarkBank to transfer the funds and aknowledge the message


# Unit testing
- Run `pytest` on the main folder


# Setup
## Setup Google Cloud and CLI
1. Create a new project in Google Cloud, install the CLI and authorize it
## .env file
```
BASE_URL=https://sandbox.api.starkbank.com
GOOGLE_PROJECT_ID=[you project id]
GOOGLE_REGION=southamerica-east1
```
## StarkBank keys
1. Run the `python stark_setup.py` script to generate a brand new public and private keys
2. Register the public key with Stark Bank as new Project



# Deploy
1. Install Google Cloud CLI and configure with the project
***Im running on a Mac in a arm architecture, we need to use buildx to target linux/amd64 to be used in GC***
2. Run `docker buildx create --name teste289594 --use` to setup the docker builder
3. Run `docker buildx inspect --bootstrap` to init buildx
4. Run `gcloud pubsub topics create invoice-payed` to create the pub/sub topic
## Google Cloud Artifact
1. Install Docker and run it
2. Create a Google Cloud Artifact Repository for the Docker images
```
gcloud artifacts repositories create teste289594-docker --repository-format=docker \
--location=southamerica-east1 --description="Docker repository"
```
3. Run `gcloud auth configure-docker southamerica-east1-docker.pkg.dev` to set as default artifact repo for your docker installation
## Deploy invoice_spammer JOB
1. Run `./deploy_invoice_spamer.sh` bash script, it will create the docker image, upload it to GC Artifact Repo and deploy it as a GC Run Job
2. Go to Google Cloud Run web interface
3. Select the invoice-spamer job
4. Select triggers and add scheduler trigger
5. Input `0 * * * *` as unix-cron field and save
*** This will make the service run every hour, setup an alerm to pause it after 24hours using the GC interface***

## Deploy money_sender service
1. Run `./deploy_money_sender.sh` bash script, it will create the docker image, upload it to GC Artifact Repo and deploy it as a GC Run Service
2. Copy the URL of the deployed service