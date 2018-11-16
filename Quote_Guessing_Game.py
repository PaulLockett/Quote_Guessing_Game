''' 
Import moduales for the webscraper and random choices
'''
import requests
from bs4 import BeautifulSoup
from random import choice
from time import sleep

print("Welcome to QuoteMatch!")
print("\nThe game where you are given a quote and have to tell us who the Author is.")
print("it talkes this game about 30 seconds to start so please wait.")
# make a list to hold the quotes
quotes_List = []

#first call to website
response = requests.get("http://quotes.toscrape.com/")
soup = BeautifulSoup(response.text, "html.parser")
quotes = soup.find_all("div",class_="quote")

#add list of quotes to the list
for quote in quotes:
	quotes_List.append(dict({
						'Text' : quote.find('span').get_text(),
						"Author" : quote.find('small',class_="author").get_text(),
						"Author_Link" : quote.find('a')['href']
						}))

# Call for the rest of the pages
for page_num in range(2,11):
	sleep(3)
	site = "http://quotes.toscrape.com/page/" + str(page_num) + "/"
	response = requests.get(site)
	soup = BeautifulSoup(response.text, "html.parser")
	quotes = soup.find_all("div",class_="quote")

	#add list of quotes to the list
	for quote in quotes:
		quotes_List.append(dict({
							'Text' : quote.find('span').get_text(),
							"Author" : quote.find('small',class_="author").get_text(),
							"Author_Link" : quote.find('a')['href']
							}))
# Game Logic
gameover = False
wins = 0

# Main gameplay loop
while(not gameover):
	#reset varables and gets random quote
	current_quote_data = choice(quotes_List)
	author_found = False
	num_trys = 4

	# loop for tries at identification
	while(not author_found and num_trys > 0):
		print("\n",current_quote_data['Text'])

		# hints
		if num_trys == 3:
			response = requests.get("http://quotes.toscrape.com/" + current_quote_data["Author_Link"])
			soup = BeautifulSoup(response.text, "html.parser")
			bday = soup.find_all("p")
			print("\nhint: ",bday[1].get_text())
		if num_trys == 2:
			print("\nhint: The first letter in their name is",current_quote_data['Author'][0])
		if num_trys == 1:
			print("\nhint: the Author's name has",len(current_quote_data['Author']),"characters in it.")
		
		# prompt for author name
		answer = input("\nWho is the Author of this quote: ")

		# check for correct and remove quote from list or decrement tries
		if answer == current_quote_data['Author']:
			author_found = True
			print("Correct! Great Job\n")
			wins += 1
			quotes_List.remove(current_quote_data)
		else:
			num_trys -= 1

	# print loss statement
	if num_trys <= 0:
		print("\nYou lose, The Author was:",current_quote_data['Author'],"\n")

	# ask if user want to play again
	play_again = input("\nWould you like to play again? y/n ")
	if play_again[0] == "n" or play_again[0] == "N":
		gameover = True

# end game and print results
print("Thanks for Playing!")
print("You identified",wins,"Author's quotes")