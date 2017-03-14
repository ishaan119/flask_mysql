from oorjan import app
from oorjan import scheduler

if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)

