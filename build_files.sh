#!/bin/bash

build_process() {
  echo "Starting build process..."

  cd frontend || exit 1
  npm run vercel-build || exit 1
  npm audit fix || exit 1
  cd .. || exit 1

  pip install --upgrade pip || exit 1
  pip install -r requirements.txt || exit 1
  python3 manage.py makemigrations || exit 1
  python3 manage.py migrate || exit 1
  python3 manage.py compilemessages || exit 1

  pip install awscli || exit 1
  aws s3 mv media s3://kolorytmedia/media --recursive || exit 1

  python3 manage.py collectstatic --noinput --clear || exit 1

  # Cleanup unnecessary files
  rm -rf frontend || exit 1
  rm -rf dist/assets/img || exit 1

  # Disk usage report
  du -h --max-depth=5 | sort -rh || exit 1
}

attempt=1
max_attempts=3

while [ $attempt -le $max_attempts ]; do
  echo "Build attempt $attempt of $max_attempts..."
  build_process && exit 0
  echo "Build failed on attempt $attempt. Retrying..."
  attempt=$((attempt + 1))
done

echo "Build failed after $max_attempts attempts."
exit 1
