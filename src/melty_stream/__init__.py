"""MeltyStream API and HTTPS Server"""
import api

if __name__ == "__main__":
    app = api.create_app()
    app.run()
