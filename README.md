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

# Setup

## Create a .env file
```
BASE_URL=https://sandbox.api.starkbank.com
```
## Create your keys
1. Run the `python setup.py` script to generate a brand new public and private keys

# Deploy

1. Install Google Cloud CLI and configure with the project
2. Deploy InvoiceSpamer Job to Cloud Run
```
gcloud run deploy invoice-spamer --source ./InvoiceSpamer --region=southamerica-east1
```
3. Deploy MoneySender Service to Cloud Run
```
gcloud run deploy money-sender --source=MoneySender --region=southamerica-east1
```
4. Deploy InvoiceUpdater Service to Cloud Run
```
gcloud run deploy invoice-updater --source ./InvoiceUpdater --region=southamerica-east1
```