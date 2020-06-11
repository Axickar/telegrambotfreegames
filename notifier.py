from datetime import datetime
import telegram

from selenium import webdriver

import time

def main():
	# Gets the current date and time
	now = datetime.now()
	current_time = now.strftime('%H:%M:%S %d/%m/%Y ')
	with open('notifierLog.txt', 'a+') as log:
		log.write('Notifier started running at: ' + current_time + '\n')

	# Strings to append games to as they are found 
	free_games_message = 'The following game(s) are currently free in the Epic Games Store: ' + '\n'
	coming_soon_message = 'These are the game(s) coming soon for free in the Epic Games Store: ' + '\n'

	# Array of user ids, I got the IDs for my friends and myself using this bot https://github.com/nadam/userinfobot
	chat_ids = ['USER IDS']

	# The token of your telegram bot, can find this using BotFather
	bot = telegram.Bot(token='YOUR TELEGRAM BOT TOKEN')

	url = 'https://www.epicgames.com/store/en-US/free-games'

	# Opens Firefox and goes to the Epic Games Store
	driver = webdriver.Firefox()
	driver.get(url)
	assert 'Epic Games Store' in driver.title

	# adjust sleeper time if your wifi is faster than mine (3 is generally long enough)
	time.sleep(10)
	# div which holds all of the free games
	mainDiv = driver.find_element_by_xpath('/html/body/div/div/div[4]/main/div/div/div/div/div[2]/div[2]/span/div/div/section/div')
	# children of mainDiv which are the free games
	indGames = mainDiv.find_elements_by_xpath('//*[@id="dieselReactWrapper"]/div/div[4]/main/div/div/div/div/div[2]/div[2]/span/div/div/section/div/*')

	for game in range(0, len(indGames)):
		# Search for same divs as above due to page reload at end of the loop
		clickMainDiv = driver.find_element_by_xpath('/html/body/div/div/div[4]/main/div/div/div/div/div[2]/div[2]/span/div/div/section/div')
		clickGames = clickMainDiv.find_elements_by_xpath('//*[@id="dieselReactWrapper"]/div/div[4]/main/div/div/div/div/div[2]/div[2]/span/div/div/section/div/*')

		clickGames[game].click()
		current_game = driver.current_url
		
		try:	
			# again, adjust sleeper time if your wifi is faster
			time.sleep(10)
			getButton = driver.find_element_by_xpath('/html/body/div/div/div[4]/main/div/div/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div/div/div[2]/span')
			free_games_message = free_games_message + current_game + '\n'
		except:
			if (driver.current_url == url):
				coming_soon_message = coming_soon_message + 'Mystery hidden game \n'
			else:
				coming_soon_message = coming_soon_message + current_game + '\n'
			
		driver.get(url)
		time.sleep(10)
		
	driver.close()

	now = datetime.now()
	current_time = now.strftime('%H:%M:%S %d/%m/%Y ')
	with open('notifierLog.txt', 'a+') as log:
		log.write('Created all the links at: ' + current_time + '\n')

	# Sends message to every user id in chat_ids
	for st in chat_ids:
		bot.send_message(chat_id=st, text=free_games_message + '\n\n' + coming_soon_message, disable_web_page_preview=True)

	now = datetime.now()
	current_time = now.strftime('%H:%M:%S %d/%m/%Y ')
	with open('notifierLog.txt', 'a+') as log:
		log.write('Notifier successfully ran at: ' + current_time + '\n')
		
if __name__ == "__main__':
	main()
	