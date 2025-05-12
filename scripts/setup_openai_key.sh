#!/bin/bash

# Script to help users set up their OpenAI API key
# This is a companion tool for the CodexContinueGPT application

set -e # Exit on error

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}======================================================${NC}"
echo -e "${CYAN}       OpenAI API Key Setup for CodexContinueGPT      ${NC}"
echo -e "${CYAN}======================================================${NC}\n"

echo -e "${YELLOW}This script will help you configure your OpenAI API key for the application.${NC}\n"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found.${NC}"
    echo -e "Creating a new .env file from template.env...\n"
    
    if [ -f template.env ]; then
        cp template.env .env
        echo -e "${GREEN}Created .env file from template.${NC}\n"
    else
        echo -e "${RED}Error: template.env file not found.${NC}"
        echo -e "Creating a minimal .env file...\n"
        
        cat > .env << EOF
# CodexContinueGPT Environment Configuration
# Created by setup_openai_key.sh

ENV=development
PYTHONPATH=/app
BACKEND_HOST=backend
BACKEND_PORT=8000

# LLM API Keys
OPENAI_API_KEY=
EOF
        echo -e "${GREEN}Created minimal .env file.${NC}\n"
    fi
fi

# Check if OpenAI API key is already set and valid
CURRENT_KEY=$(grep "OPENAI_API_KEY" .env | cut -d= -f2- | xargs)

if [[ "$CURRENT_KEY" != "" && "$CURRENT_KEY" != "your-openai-api-key-here" && "$CURRENT_KEY" != "your_openai_api_key_here" ]]; then
    echo -e "${YELLOW}You already have an OpenAI API key configured:${NC}"
    echo -e "Current key: ${CURRENT_KEY:0:3}...${CURRENT_KEY: -4}\n"
    
    read -p "Do you want to change it? (y/N): " change_key
    if [[ "$change_key" != "y" && "$change_key" != "Y" ]]; then
        echo -e "\n${GREEN}Keeping existing API key.${NC}"
        exit 0
    fi
fi

echo -e "${YELLOW}To get your OpenAI API key:${NC}"
echo "1. Visit https://platform.openai.com/account/api-keys"
echo "2. Sign in to your OpenAI account (or create one)"
echo -e "3. Generate a new API key\n"

read -p "Enter your OpenAI API key: " api_key

if [ -z "$api_key" ]; then
    echo -e "\n${RED}Error: API key cannot be empty.${NC}"
    exit 1
fi

# Update the API key in the .env file
if grep -q "OPENAI_API_KEY=" .env; then
    # Replace existing line
    sed -i.bak "s|OPENAI_API_KEY=.*|OPENAI_API_KEY=$api_key|" .env
    rm -f .env.bak
else
    # Add new line
    echo "OPENAI_API_KEY=$api_key" >> .env
fi

echo -e "\n${GREEN}✅ Successfully updated OpenAI API key in .env file.${NC}"
echo -e "\n${YELLOW}Note: You'll need to restart your services for changes to take effect:${NC}"
echo -e "  docker-compose restart backend"

# If docker-compose is running, offer to restart the backend service
if command -v docker-compose &> /dev/null; then
    if docker-compose ps | grep -q "backend.*Up"; then
        echo -e "\n${YELLOW}The backend service is currently running. Would you like to restart it now?${NC}"
        read -p "Restart backend? (y/N): " restart_backend
        
        if [[ "$restart_backend" == "y" || "$restart_backend" == "Y" ]]; then
            echo -e "\n${CYAN}Restarting backend service...${NC}"
            docker-compose restart backend
            echo -e "${GREEN}Backend service restarted. Changes should now be active.${NC}"
        fi
    fi
fi

echo -e "\n${CYAN}======================================================${NC}"
echo -e "${GREEN}Setup complete! You can now use the application with your OpenAI API key.${NC}"
echo -e "${CYAN}======================================================${NC}\n"
