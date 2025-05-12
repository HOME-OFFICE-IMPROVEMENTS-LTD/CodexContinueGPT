# API Key Configuration Guide for CodexContinueGPT

There are multiple ways to configure API keys in CodexContinueGPT, depending on your use case and preferences. This guide outlines all available methods.

## 1. Using the Setup Script (Recommended for New Users)

The easiest way to configure your OpenAI API key is to use our helper script:

```bash
# Make the script executable (if not already)
chmod +x scripts/setup_openai_key.sh

# Run the setup script
./scripts/setup_openai_key.sh
```

This interactive script will:
1. Ask for your API key
2. Update your `.env` file automatically
3. Offer to restart the backend service for you

## 2. Using the API Keys Page in the UI

If you prefer a graphical interface, you can use the API Keys page in the application:

1. Navigate to the "API Keys" page in the sidebar menu
2. Enter your OpenAI API key in the form
3. Select your preferred save location
4. Click "Save API Key"

## 3. Manually Editing the .env File

For direct configuration, you can edit the `.env` file in the project root directory:

1. Open the `.env` file in a text editor:
   ```bash
   nano .env
   ```

2. Find the `OPENAI_API_KEY` line and update it with your actual API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

3. Save the file and restart the backend service:
   ```bash
   docker-compose restart backend
   ```

## 4. Setting Environment Variables

You can also set the API key as an environment variable, which is useful for temporary usage or CI/CD pipelines:

```bash
# For Linux/macOS
export OPENAI_API_KEY=sk-your-actual-api-key-here

# For Windows Command Prompt
set OPENAI_API_KEY=sk-your-actual-api-key-here

# For Windows PowerShell
$env:OPENAI_API_KEY = "sk-your-actual-api-key-here"
```

Remember to set this variable before starting the application or the container.

## 5. Using Docker Environment Variables

When using Docker Compose, you can set the environment variable in your `docker-compose.yml` file:

```yaml
services:
  backend:
    # ... other configuration ...
    environment:
      - OPENAI_API_KEY=sk-your-actual-api-key-here
```

Or pass it when starting the container:

```bash
docker-compose up -d -e OPENAI_API_KEY=sk-your-actual-api-key-here
```

## Where to Get API Keys

### OpenAI API Key
- Visit: https://platform.openai.com/account/api-keys
- Sign up or log in to your OpenAI account
- Click "Create new secret key"
- Copy the key immediately (you won't be able to see it again)

### Other API Keys (Optional)

CodexContinueGPT supports other LLM providers that you can configure in the same ways:

- **Anthropic API Key** (`ANTHROPIC_API_KEY`): https://console.anthropic.com/
- **Cohere API Key** (`COHERE_API_KEY`): https://dashboard.cohere.com/api-keys

## Troubleshooting

If you're experiencing issues with your API key:

1. **Verify the Key Format**: OpenAI API keys typically start with `sk-` and are about 50 characters long.

2. **Check for Error Messages**: Look for specific error messages in the application logs or UI.

3. **Restart Services**: Sometimes a full restart is needed:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

4. **Check Billing Status**: Ensure your OpenAI account has active billing and enough credits.

5. **API Key Quotas**: Be aware of rate limits and quotas associated with your API key.

## Security Best Practices

- Never commit API keys to version control
- Consider using environment variables for production deployments
- Rotate API keys periodically for security
- Set up billing limits in your OpenAI account to prevent unexpected charges
