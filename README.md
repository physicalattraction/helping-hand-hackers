# helping-hand-hackers
Hackathon for Good - Red Cross challenge

By:
- [Gabor Kocsi](https://github.com/kocsigabor99)
- [Marin Chiosa](https://github.com/MarinChiosa246602)
- [Mate Kovasznai](https://github.com/MateKovasznai241960)
- [Erwin Rossen](https://github.com/physicalattraction)

## Usage notes

1. In `src`, create a file called secrets.json` with the following content:
```json
{
  "OPENAI_KEY": "sk-proj-...bwUA",
  "GEMINI_KEY": "..."
}
```
2. Make sure you have a virtual environment up and running.
3. Install the required packages from the root directory with
```
pip install -r requirements.txt
```
4. Run the Chatbot from the `src` directory with 
```
python -m redcross-chatbot
```

## Repository structure

Used in final presentation:
- `src/redcross-chatbot.py`: The main script for the chatbot. Run this module to run the chatbot
- `src/redcross-website.py`: We used this script to convert the Excel sheet with the Red Cross data to a readable CSV file
- `data/chatbot-input/chatbot-input.csv`: The result from the script above, used for the prompt
- `src/utils.py`: Directory structure helpers

Not used in final presentation:
- `src/RedCrossChatbot`: A Django application that we started to build as an API for an interface we were building. In the end, we didn't use this because of time constraints and issues we faced with tokens
- `src/self-trained-chatbot.py`: A script we used to train the chatbot on the data from the Red Cross. We didn't use this in the end, because the result out-of-the-box was not good enough, and it would take too much time to train a proper model
