"""Punto de entrada para desarrollo: python run.py → http://localhost:5000"""
from fancyhotel import create_app

app = create_app()

if __name__ == "__main__":
    # Sólo localhost: el modo debug de Flask permite ejecutar código desde el navegador.
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
