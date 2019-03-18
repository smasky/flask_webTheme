import os


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')


from SmaBlog import create_app  # noqa
from flask_script import Manager

app = create_app('production')

manager = Manager(app)  
  
if __name__ == '__main__':  
    manager.run() 