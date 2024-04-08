
#!/bin/bash

# Assuming frontend assets are generated into myshop/frontend/dist
FRONTEND_DIR="myshop/frontend"

# Check if frontend directory exists
if [ -d "$FRONTEND_DIR" ]; then
    echo "Frontend directory exists. Continuing with deployment..."
    # Perform deployment steps here (e.g., copying assets to appropriate location)
else
    echo "Error: Frontend directory '$FRONTEND_DIR' not found."
    exit 1
fi
# Build the project
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Make Migration..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear