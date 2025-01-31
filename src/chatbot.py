import os

from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, \
    DataCollatorForLanguageModeling

from utils import CHATBOT_INPUT_DIR, CHATBOT_MODELS_DIR


class ChatBot:
    def __init__(self, data_folder, model_name='gpt2', model_filename='redcross',
                 force_train=False):
        self.data_folder = data_folder
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model_path = os.path.join(CHATBOT_MODELS_DIR, model_filename)
        if os.path.exists(self.model_path) and not force_train:
            self.load_model()
        else:
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.train_model()
            self.save_model()

    def load_documents(self):
        documents = ""
        for filename in os.listdir(self.data_folder):
            if filename.endswith('chatbot-input.csv'):
                with open(os.path.join(self.data_folder, filename), 'r') as file:
                    documents += file.read() + "\n"
        return documents

    def train_model(self):
        documents = self.load_documents()
        if not documents.strip():
            raise ValueError("No documents found in the data folder.")

        with open('train.txt', 'w') as f:
            f.write(documents)

        dataset = load_dataset('text', data_files='train.txt')
        if len(dataset['train']) == 0:
            raise ValueError("The dataset is empty. Please ensure 'train.txt' contains data.")

        tokenized_dataset = dataset.map(
            lambda e: self.tokenizer(e['text'], truncation=True, padding='max_length', max_length=128), batched=True)

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )

        training_args = TrainingArguments(
            output_dir='./results',
            overwrite_output_dir=True,
            num_train_epochs=5,
            per_device_train_batch_size=4,
            save_steps=10_000,
            save_total_limit=2,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=tokenized_dataset['train'],
        )

        trainer.train()

    def save_model(self):
        self.model.save_pretrained(self.model_path)
        self.tokenizer.save_pretrained(self.model_path)

    def load_model(self):
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)

    def answer_question(self, question):
        inputs = self.tokenizer.encode(question, return_tensors='pt').to(self.model.device)
        outputs = self.model.generate(inputs, max_length=100, num_return_sequences=1)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer


# Example usage
if __name__ == "__main__":
    chatbot = ChatBot(data_folder=CHATBOT_INPUT_DIR, model_filename='redcross',
                      force_train=True)
    while True:
        question = input("Ask a question: ")
        if question.lower() in ['exit', 'quit']:
            break
        answer = chatbot.answer_question(question)
        print(answer)
