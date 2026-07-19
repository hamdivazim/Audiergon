# Self-hosting Audiergon Frontend

If you want to self host Audiergon, you can deploy the CDK stack (use instructions in `cloud/aws/README.md`) and use the outputted API URL result directly at [https://audiergon.hamdtel.co.uk/](https://audiergon.hamdtel.co.uk/). However if you would like, you can self host the frontend too.

## Prerequisites

Before getting started, make sure you have the following installed on your machine:
* Node.js
* npm or yarn / pnpm
* A deployed Audiergon API Gateway URL (from your CDK deployment output)

## Environment Setup

The frontend relies on an environment variable to locate your API backend. 

1. Create a file named `.env.local` in the `cloud\frontend\audiergon-cloudfrontend` directory:
   ```bash
   touch .env.local
   ```
2. Add the following line to `.env.local`:
```
NEXT_PUBLIC_API_URL=https://[YOUR-API-URL].execute-api.us-east-1.amazonaws.com/equalise
```
3. Install dependencies:
```bash
cd cloud/frontend/audiergon-cloudfrontend
npm install
```

## Local Development
Start the local Next.js dev server:
```bash
npm run dev
```

## Production Build & Deployment
I recommend using Vercel to deploy.
1. Install Vercel CLI
```bash
npm install -g vercel
```
2. Run the deployment from `cloud/frontend/audiergon-cloudfrontend`
```bash
vercel
```

## Contributing to Audiergon Cloud Frontend

This is a simple lightweight frontend designed to be easily usable both as a ready-to-go demo of Audiergon and to self host for your own EQ or DSP tasks. Contributions are very welcome, so take a look in the root README if you'd like to add to Audiergon :)