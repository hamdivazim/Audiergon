# Audiergon Cloud
You can use my [hosted instance](https://audiergon.hamdtel.co.uk/) online at any time, or you can host your own.

## AWS Architecture
For an explanation on how Audiergon Cloud was architected with AWS, check out `cloud\aws\ARCHITECTURE.md`

## Prerequisites
* Node.js
* AWS CLI configured with your credentials (`aws configure`)
* AWS CDK CLI (`npm install -g aws-cdk`)
* Cloned copy of Audiergon (`git clone https://github.com/hamdivazim/Audiergon.git`)

## CDK Deployment
Navigate to your CDK directory and install the required packages:
```bash
cd cdk
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Bootstrap CDK if you have never used it in your current region:
```bash
cdk bootstrap
```
Synthesise and deploy the CDK stack
```bash
cdk deploy
```
The command line will contain an output for an API URL. Copy it into the frontend through the settings button.

## Modifying Limits
My hosted instance of Audiergon has a 5s limit on audio length. To change these, go to `cloud/lambda/handler.py` and change line 40 to any limit you want. Keep in mind that you may need to raise the allocated memory (and CPU) for Lambda. Change this in the CDK stack Python file.

## Tearing Down Resources
If you no longer need a self-hosted instance of Audiergon, use the following command:
```bash
cdk destroy
```