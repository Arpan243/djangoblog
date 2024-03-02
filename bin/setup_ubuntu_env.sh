python3 -m venv env
activate() {
    . env/bin/activate
    echo "installing requirements to virtual environment"
    pip install -r requirements.txt
}
activate