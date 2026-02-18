# ============================
# FASTAPI BACKEND DEPLOY SCRIPT
# ============================

# --- CONFIGURATION ---
$resourceGroup = "caseyemerydev-rg"
$containerApp = "fastapi-app-container"
$acrName = "aichatappcontainer"
$imageName = "fastapi-app"

# --- AUTO-GENERATED TAGS ---
# Incremental build number based on timestamp (sortable + unique)
$timestampTag = (Get-Date -Format "yyyyMMdd-HHmmss")

# Optional: Git commit hash (short)
$gitHash = (git rev-parse --short HEAD) 2>$null

# Final tag combines timestamp + git hash if available
if ($gitHash) {
    $tag = "$timestampTag-$gitHash"
} else {
    $tag = "$timestampTag"
}

Write-Host "Using image tag: $tag"

# --- LOGIN TO AZURE ---
Write-Host "Logging into Azure..."
az login

# --- LOGIN TO ACR ---
Write-Host "Logging into Azure Container Registry..."
az acr login --name $acrName

# --- BUILD DOCKER IMAGE (NO CACHE) ---
Write-Host "Building Docker image..."
docker build --no-cache -t "${imageName}:${tag}" .

# --- TAG IMAGE FOR ACR ---
Write-Host "Tagging image..."
docker tag "${imageName}:${tag}" "$acrName.azurecr.io/${imageName}:${tag}"

# --- PUSH IMAGE TO ACR ---
Write-Host "Pushing image to Azure Container Registry..."
docker push "$acrName.azurecr.io/${imageName}:${tag}"

# --- UPDATE CONTAINER APP TO NEW IMAGE ---
Write-Host "Updating Azure Container App to new image..."
az containerapp update `
  --name $containerApp `
  --resource-group $resourceGroup `
  --image "$acrName.azurecr.io/${imageName}:${tag}"

Write-Host "Deployment complete!"

# --- OPTIONAL CLEANUP: REMOVE OLD LOCAL IMAGES ---
Write-Host "Cleaning up old local Docker images..."
docker image prune -f