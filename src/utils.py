import os.path

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
CHATBOT_INPUT_DIR = os.path.join(DATA_DIR, 'chatbot-input')
CHATBOT_MODELS_DIR = os.path.join(DATA_DIR, 'chatbot-models')
