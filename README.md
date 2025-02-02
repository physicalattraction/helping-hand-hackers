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

## Examples

### OpenAI
You: Where can I sleep tonight?

Bot: You have several options for sleeping tonight:

1. **LVV Rotterdam**: If you have received a negative decision for asylum, you can visit the LVV office for help and advice regarding 24-hour shelter. They can assist you with entering the LVV program. You can contact them at Phone: 14 010 or Email: vreemdelingenloketMO@rotterdam.nl. [More Information](shelter/night-shelter/lvv-rotterdam)
2. **Winter Cold Regulation in Delft**: If you are in Delft and it is particularly cold tonight, you can access the winter shelter, which is open for all homeless people. Please note that it opens from January 31st. You can contact them at Phone: (+)31 1 52 84 10 68 or Email: info@perspektief.nl. [More Information](shelter/night-shelter/winter-shelter-delft)
3. **Winter Cold Regulation The Hague**: In The Hague, there is a night shelter available for all homeless people when it is too cold to sleep outside. It also opens from January 31st. Unfortunately, there is no contact information available. [More Information](shelter/night-shelter/winter-shelter)
4. **For immediate shelter on Saturdays**: The World House and the Red Cross provide a place to stay during the winter months every Saturday. 

Make sure to check the details and reach out if you need more help!

### Gemini
You: Where can I sleep tonight?

Bot: That depends on your circumstances and location.  To best help you, I need some more information.  However, here are some possibilities based on my knowledge base:

* **If you are in Rotterdam and received a negative asylum decision:**  You can contact LVV Rotterdam. They might be able to help you find 24-hour shelter.  [shelter/night-shelter/lvv-rotterdam]  Phone: 14 010. Email: vreemdelingenloketMO@rotterdam.nl
* **If it's very cold and you're in Delft:** The winter cold shelter may be open.  It opens on January 31st and is for anyone experiencing homelessness. [shelter/night-shelter/winter-shelter-delft] Phone: (+)31 1 52 84 10 68. Email: info@perspektief.nl
* **If it's very cold and you are in The Hague:** The winter night shelter in The Hague might be an option, but it only opens when temperatures are dangerously low and opens on January 31st. [shelter/night-shelter/winter-shelter]  (Note: Phone and email are currently unknown.)
* **If you need a night shelter and none of the above apply:** I don't currently have information on other night shelters.  You may wish to try contacting the Red Cross helpline [where-to-go-first/go-first/helpline] to see if they can assist you in finding a place to sleep.
Please provide me with more information about your location and situation, so I can offer more targeted advice.

### Gemini in Dutch
You: Ik heb honger!

Bot: Ik begrijp dat je honger hebt!  Er zijn verschillende plaatsen in Den Haag waar je gratis eten kunt krijgen.  Afhankelijk van de dag en het tijdstip, zijn er verschillende opties:

* **Soepbus bij Koekamp (bij het centraal station):** Hier kun je soep en een warme drank krijgen.  (/food-clothing/food/soepbus)
* **Straatpastoraat (Stadsklooster):** Elke vrijdagavond (vanaf 18:00 uur) serveren ze een gratis maaltijd.  (/food-clothing/food/straatpastoraat)
* **Gratis ontbijt op zaterdag:**  Je kunt elke zaterdagmorgen tussen 09:30 en 11:00 uur een gratis ontbijt krijgen aan de Dunne Bierkade 16. (/food-clothing/food/breakfast-saturday)
* **Gratis lunch op zaterdag:**  Je kunt elke zaterdag rond de middag (12:00 uur) een gratis lunch krijgen bij het winterweekendopvang in The Hague World House. (/food-clothing/food/free-lunch-saturdays)
* **Sociaal Restaurant Vadercentrum:** Hier kun je ook een gratis maaltijd nuttigen.  (/food-clothing/food/social-restaurant)

Voor meer informatie over voedselhulp, kun je ook kijken naar: (/food-clothing/food) 

Ik hoop dat dit helpt! Laat me weten of je nog andere vragen hebt.
