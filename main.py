from repository import Repository
from app import App

try:
    rep = Repository()
    app = App(rep)
    app.run()
except Exception as error:
    print(f"Error: {error}")
finally:
    rep.close_connection()
