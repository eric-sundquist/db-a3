from repository import Repository
from app import App


try:
    rep = Repository()
    app = App(rep)
    app.run()
except Exception as error:
    print("There was an Error")
    print(error)
    print(error.with_traceback)
finally:
    rep.close_connection()
