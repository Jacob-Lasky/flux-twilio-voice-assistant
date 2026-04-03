#!/bin/bash
set -euo pipefail

# --- Stop helper for Podman ---
# - Stops and removes the 'dg-drinks' container
# - Optionally stops the Podman VM

echo "🛑 Stopping 'dg-drinks' container..."
podman stop dg-drinks >/dev/null 2>&1 || true
podman rm dg-drinks   >/dev/null 2>&1 || true

echo "✅ Container stopped and removed."

# Ask if user also wants to stop Podman VM
read -p "Do you also want to stop the Podman VM? (y/N): " yn
case $yn in
    [Yy]* ) 
        echo "🛑 Stopping Podman VM..."
        podman machine stop
        echo "✅ Podman VM stopped."
        ;;
    * ) 
        echo "ℹ️ Podman VM left running."
        ;;
esac
