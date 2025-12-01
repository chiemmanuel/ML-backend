# Create venv

python -m venv venv    

# Activate venv

.\venv\Scripts\activate

# Install base depencies

pip install wheel setuptools
pip install cmake  

# cd into working directory (or not)

cd yolo     

# Upgrade pip

label_studio_ml_backend\venv\Scripts\python.exe -m pip install --upgrade pip

# Install requirements base and requirements

pip install -r requirements-base.txt
pip install -r requirements.txt

# Install dependencies outside de requirement files

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

pip install ultralytics  

pip install waitress

# Run server

waitress-serve --host=0.0.0.0 --port=9090 _wsgi:app
