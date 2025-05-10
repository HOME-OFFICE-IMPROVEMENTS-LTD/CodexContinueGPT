#!/bin/bash

# Test script to verify Docker configuration
# Last Updated: 2025-05-09

# Terminal colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
echo -e "${YELLOW}🐳 Testing Docker Configuration 🐳${NC}"
echo -e "${YELLOW}----------------------------------------${NC}"

# Check if Docker is installed and running
echo -e "${BLUE}Testing Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed or not in PATH${NC}"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is not running${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is installed and running${NC}"
DOCKER_VERSION=$(docker --version)
echo -e "   ${BLUE}$DOCKER_VERSION${NC}"

# Check if docker-compose is installed
echo -e "${BLUE}Testing Docker Compose installation...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed or not in PATH${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker Compose is installed${NC}"
COMPOSE_VERSION=$(docker-compose --version)
echo -e "   ${BLUE}$COMPOSE_VERSION${NC}"

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check for the presence of required files
echo -e "${BLUE}Checking required Docker configuration files...${NC}"
files_to_check=(
    "$PROJECT_ROOT/Dockerfile"
    "$PROJECT_ROOT/.devcontainer/Dockerfile"
    "$PROJECT_ROOT/.devcontainer/devcontainer.json"
    "$PROJECT_ROOT/docker-compose.yml"
    "$PROJECT_ROOT/.env.production"
    "$PROJECT_ROOT/.env.development"
    "$PROJECT_ROOT/scripts/switch_env.sh"
)

all_files_present=true
for file in "${files_to_check[@]}"; do
    basename=$(basename "$file")
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ Missing file: $basename${NC}"
        all_files_present=false
    else
        echo -e "${GREEN}✅ File exists: $basename${NC}"
    fi
done

if [ "$all_files_present" = false ]; then
    echo -e "${RED}❌ Some required files are missing${NC}"
    exit 1
fi

# Validate docker-compose.yml
echo -e "${BLUE}Validating docker-compose.yml...${NC}"
if ! docker-compose -f "$PROJECT_ROOT/docker-compose.yml" config > /dev/null 2>&1; then
    echo -e "${RED}❌ docker-compose.yml validation failed${NC}"
    docker-compose -f "$PROJECT_ROOT/docker-compose.yml" config
    exit 1
else
    echo -e "${GREEN}✅ docker-compose.yml is valid${NC}"
fi

# Check environment files content
echo -e "${BLUE}Checking environment files...${NC}"
if grep -q "ENV=development" "$PROJECT_ROOT/.env.development"; then
    echo -e "${GREEN}✅ .env.development has correct ENV variable${NC}"
else
    echo -e "${RED}❌ .env.development is missing ENV=development${NC}"
fi

if grep -q "ENV=production" "$PROJECT_ROOT/.env.production"; then
    echo -e "${GREEN}✅ .env.production has correct ENV variable${NC}"
else
    echo -e "${RED}❌ .env.production is missing ENV=production${NC}"
fi

echo -e "${YELLOW}----------------------------------------${NC}"
echo -e "${GREEN}🚀 Docker configuration verification complete!${NC}"

# Show current environment
if [ -f "$PROJECT_ROOT/.env" ]; then
    ENV_TYPE=$(grep "ENV=" "$PROJECT_ROOT/.env" | head -1 | cut -d'=' -f2)
    echo -e "${YELLOW}Current environment:${NC} $ENV_TYPE"
else
    echo -e "${YELLOW}No .env file found. Please run switch_env.sh to create one.${NC}"
fi

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "  1. Run '${YELLOW}./scripts/switch_env.sh dev${NC}' to use development environment"
echo -e "  2. Run '${YELLOW}./scripts/switch_env.sh prod${NC}' to use production environment"
echo -e "  3. Build and run with: '${YELLOW}docker-compose build && docker-compose up -d${NC}'"
echo -e "  4. Or use VS Code tasks for Docker operations"
echo -e "${YELLOW}----------------------------------------${NC}"

exit 0
