python -m venv env
activate() {
    source ./env/Scripts/activate
    echo "installing requirements to virtual environment"
    pip install -r requirements.txt
}
activate