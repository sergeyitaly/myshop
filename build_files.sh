# build_files.sh
python3.9 -m venv myenv  # Create a virtual environment named 'myenv'
source myenv/bin/activate  # Activate the virtual environment

pip install -r requirements.txt
python3.9 manage.py collectstatic