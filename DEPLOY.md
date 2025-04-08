# Deploying the Restaurant Menu MCP Server

This guide explains how to deploy the MCP server to various cloud platforms.

## Prerequisites

1. Docker installed on your local machine
2. A cloud platform account (Google Cloud, AWS, or Azure)
3. Required environment variables:
   - `BASE_URL_ECOM_V2`
   - `AUTHORIZATION`
   - `UUID`

## Local Testing

1. Build the Docker image:
```bash
docker build -t restaurant-menu-mcp .
```

2. Run the container locally:
```bash
docker run -p 8000:8000 \
  -e BASE_URL_ECOM_V2=your_url \
  -e AUTHORIZATION=your_auth \
  -e UUID=your_uuid \
  restaurant-menu-mcp
```

## Google Cloud Run Deployment

1. Install Google Cloud SDK and initialize:
```bash
gcloud init
```

2. Enable required APIs:
```bash
gcloud services enable run.googleapis.com
```

3. Build and push the image to Google Container Registry:
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/restaurant-menu-mcp
```

4. Deploy to Cloud Run:
```bash
gcloud run deploy restaurant-menu-mcp \
  --image gcr.io/YOUR_PROJECT_ID/restaurant-menu-mcp \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars="BASE_URL_ECOM_V2=your_url,AUTHORIZATION=your_auth,UUID=your_uuid"
```

## Updating claude_desktop_config.json

After deploying, update your `claude_desktop_config.json` to use the remote server:

```json
{
  "mcpServers": {
    "Demo": {
      "url": "https://your-deployed-url",
      "headers": {
        "Content-Type": "application/json"
      }
    }
  }
}
```

Replace `https://your-deployed-url` with:
- For Google Cloud Run: The URL provided after deployment
- For AWS: Your API Gateway URL
- For Azure: Your App Service URL

## Health Check

Test the deployed server:
```bash
curl -X POST https://your-deployed-url \
  -H "Content-Type: application/json" \
  -d '{
    "method": "get_restaurant_menu",
    "params": {
      "restaurant_id": 123,
      "branch_id": 456,
      "brand_id": "789"
    }
  }'
```

## Troubleshooting

1. If you get connection errors:
   - Verify the server URL is correct
   - Check if the server is running (Cloud Run logs)
   - Verify environment variables are set correctly

2. If you get authentication errors:
   - Verify your environment variables are correctly set
   - Check if the service account has necessary permissions

3. If the server doesn't respond:
   - Check the server logs in your cloud platform
   - Verify the port configuration
   - Check if the container is healthy 