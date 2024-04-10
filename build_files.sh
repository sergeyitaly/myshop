# build_files.sh
python3.9 -m venv myenv  # Create a virtual environment named 'myenv'
source myenv/bin/activate  # Activate the virtual environment

python3.9 -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic -l --noinput