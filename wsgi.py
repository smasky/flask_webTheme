import os


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')


from Smablog import create_app  # noqa

app = create_app('testing')
