# helping-hand-hackers
Hackathon for Good - Red Cross challenge

### Usage notes

1. In `src`, create a file called secrets.json` with the following content:
```json
{
  "OPENAI_KEY": "sk-proj-...bwUA"
}
```
Marin can provide you with the working API key, which ends with `...bwUA`.

2. Make sure you have a virtual environment up and running.
3. Install the required packages with 
```
pip install -r requirements.txt
```
4. Run the Chatbot with 
```
python -m chatbot.py
```