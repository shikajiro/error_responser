from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
from server import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
# export DATABASE_URL="postgresql+psycopg2:///error_responser"
