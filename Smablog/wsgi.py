import os


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')


from SmaBlog import create_app  # noqa

app = create_app('production')
