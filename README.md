# SECTION 1: PROJECT TITLE
SG FoodBot
--
![alt text](https://github.com/boonyew/ISS-CS-SGFoodBot/blob/master/poster.png)

# SECTION 2: EXECUTIVE SUMMARY
Singapore is a popular tourist destination, receiving a large number of visitors from across the world annually. Apart from famous attractions such as the Universal Studios, Marina Bay Sands, it is also home to a large, diverse and unique mix of food cuisines, which is what Singapore is also known for. Tourists in Singapore have a wide range of food options to choose from. However, tourists often have a difficult time choosing a place to have their meals as there are too many choices available and not enough information to guide them in this decision.

Hence, a solution that provides tourists with such information and recommendations may be beneficial to them, enhancing their experience here in Singapore. In this project, we develop an online chatbot using Google Dialogflow and Python that allows tourists to use during their stay in Singapore. The chatbot provides recommendations of food outlets based on tourists’ cuisine or location queries.

# SECTION 3: CREDITS/PROJECT CONTRIBUTION

| Official Full Name|Student ID| Work Scope  |Email|
|:---------:|:-------------:|:-----:|:----:|
|Ang Boon Yew| A0096966E		|Chatbot Design, DialogFlow Configuration, Flask Backend App, Handling of Zomato APIs,Integration with Telegram, App Hosting on Heroku 	|boonyew@u.nus.edu|
|Kartik Chopra|A0198483L		|Chatbot Design, DialogFlow Configuration, Flask Backend App, Handling of Zomato APIs, Initial Python Framework, Google Assistant Integration 	|kartik@u.nus.edu|
|Karamjot Singh|A0198470U		|Chatbot Design, DialogFlow Configuration, Flask Backend App, Handling of Zomato APIs, Backend Modules and Testing, Video Editing	|	singh@u.nus.edu|


# SECTION 4: VIDEO INTRODUCTION & USER GUIDE
<a href="https://github.com/boonyew/ISS-CS-SGFoodBot/blob/master/SGFoodBot_Video.mp4" target="_blank"><img src="https://github.com/boonyew/ISS-CS-SGFoodBot/blob/master/SGFoodBot_Video.jpg" 
alt="SGFoodBot" width="640" height="360" border="10" /></a>


# SECTION 5: USER GUIDE
SG FoodBot is a Google Assistant and Telegram based Chat Bot Agent using Google DialogFlow for providing suggestions of restaurants in Singapore based on the user's preferences and queries.

1. Using SG FoodBot on Google Assistant/Telegram
 Follow below steps to start using SG FoodBot:
 
- *Google Assistant*
	- Start up Google Assistant and enter/say "Talk to SG Food Bot"
	- Alteratively, click on this link: https://assistant.google.com/services/a/uid/00000079f9fd6f18?hl=en. Select "Alpha Testing" and submit. Select "Talk to SG FoodBot" to start the chatbot
	- Enter a cuisine, location, or a query like "Top 5 Chinese Restaurants"
	- Select a restaurant from the list to find out more about it
	- To start another query, select "Another Query" to restart the search function.
	- To end the conversation, select "End Convo"
	
	For iOS users, please perform the following steps:
	
	1. Copy the opt-in URL to Notes app

	2. Hold press the opt-in link then select 'Open in "Assistant"'. Google Assistant and App page in the Assistant Directory will be displayed.

	3. Scroll down the page until you see the "Become a Alpha tester" 		section

	4. Click the "I'M IN" button

	5. Test the Action

- *Telegram*
	- Search for the Telegram bot: "@sg_foodbot"
	- Enter /start to start SG FoodBot
	- Enter a cuisine, location, or a query like "Top 5 Chinese Restaurants"
	- Select a restaurant from the list to find out more about it

2.  Setting up SG FoodBot in Google DialogFlow
Follow below steps to setup SG FoodBot:

-   git clone  [https://github.com/boonyew/SGFoodBot.git](https://github.com/boonyew/SGFoodBot..git)
-   Use your web browser to navigate to DialogFlow website  [https://dialogflow.com/](https://dialogflow.com/)
-   Login to DialogFlow with your Google userid and password
-   Click 'Go to Console' to enter in to DialogFlow
-   Create a new DialogFlow Agent and Save
-   Upon successful completion of Agent Creation, Click Settings icon next to the Agent name.
-   Select 'Export and Import' Menu option in Settings page and Click 'Import From ZIP' option to import DialogFlow agent from the file "SGFoodBot.zip" downloaded from GitHub cloned project folder.
- Navigate to the testing agent on the right-hand side toolbar to test the chatbot. You can also start the chatbot in Google Assistant by entering "Talk to SG Food Bot" or through this link https://assistant.google.com/services/a/uid/00000079f9fd6f18?hl=en, as well as on Telegram by searching for "@sg_foodbot".
-   Enter questions like :
    -   "I would like to go to some Chinese restaurants"
    -   "Best restaurants in Clementi" 
    -   " Top 5 Indian restaurants in Orchard"
# SECTION 6: PROJECT REPORT
[https://github.com/boonyew/ISS-CS-SGFoodBot/blob/master/SGFoodBot_FinalReport_Team7.pdf]
