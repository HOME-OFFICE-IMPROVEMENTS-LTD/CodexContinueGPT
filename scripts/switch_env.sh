#!/bin/bash

# Helper script to switch between development and production environments
# Last Updated: 2025-05-09

# Terminal colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage information
function show_usage {
  echo -e "${BLUE}Usage: $0 [dev|prod|status]${NC}"
  echo -e "  dev    - Switch to development environment"
  echo -e "  prod   - Switch to production environment"
  echo -e "  status - Show current environment status"
  echo -e "Example: $0 dev"
}

# Function to show environment status
function show_status {
  if [ -f .env ]; then
    ENV_TYPE=$(grep "ENV=" .env | head -1 | cut -d'=' -f2)
    echo -e "${YELLOW}Current environment:${NC} $ENV_TYPE"
    echo -e "${YELLOW}Environment variables:${NC}"
    grep -v "^#" .env | sort
  else
    echo -e "${RED}No .env file found. Run '$0 dev' or '$0 prod' to create one.${NC}"
  fi
}

# Header
echo -e "${YELLOW}🐳 CodexContinueGPT Environment Switcher${NC}"
echo -e "${YELLOW}=====================================${NC}"

# Check if argument is provided
if [ $# -ne 1 ]; then
  show_usage
  exit 1
fi

# Set environment based on argument
case "$1" in
  "dev")
    echo -e "${BLUE}Switching to development environment...${NC}"
    if [ -f .env ]; then
      cp .env .env.backup
      echo -e "${GREEN}✅ Backed up current .env to .env.backup${NC}"
    fi
    cp .env.development .env
    echo -e "${GREEN}✅ Environment set to development.${NC}"
    ;;
  "prod")
    echo -e "${BLUE}Switching to production environment...${NC}"
    if [ -f .env ]; then
      cp .env .env.backup
      echo -e "${GREEN}✅ Backed up current .env to .env.backup${NC}"
    fi
    cp .env.production .env
    echo -e "${GREEN}✅ Environment set to production.${NC}"
    ;;
  "status")
    show_status
    exit 0
    ;;
  *)
    echo -e "${RED}❌ Error: Unknown option '$1'${NC}"
    show_usage
    exit 1
    ;;
esac

# Show the current status after switching
show_status

# Show next steps
echo ""
echo -e "${GREEN}🚀 Next steps:${NC}"
echo -e "  - Run '${BLUE}docker-compose build${NC}' to rebuild containers"
echo -e "  - Run '${BLUE}docker-compose up -d${NC}' to start services"
echo -e "  - Or use VS Code tasks for Docker operations"
echo ""

exit 0
