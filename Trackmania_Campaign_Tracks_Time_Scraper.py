import requests
from bs4 import BeautifulSoup

FIRST_CAMPAIGN_URL = "https://www.trackmania.com/campaigns/2020/summer"
LATEST_CAMPAIGN_URL = "https://www.trackmania.com/campaigns"

all_track_links = []
data_rows = ""

def getAllTrackLinks(url):
	print(url)
	html = requests.get(url).content
	html = BeautifulSoup(html, 'html.parser')

	links = html.find_all('a', class_='tm-map-card-official-link')
	links = [link.get('href') for link in links]

	out = []

	for link in links:
		all_track_links.append(link)

	campaign_links = html.find_all('a', class_='tm-page-hero-control')
	campaign_links = [link.get('href') for link in campaign_links]

	if  url != FIRST_CAMPAIGN_URL:
		getAllTrackLinks(campaign_links[0])


def getTrackData(url):
	data_row = ""
	html = requests.get(url).content
	html = BeautifulSoup(html, 'html.parser')



	# Get track name

	#mp-format

	header = (html.find('span', class_='mp-format')).contents[0]
	year = header.split(' ')[1].split(' ')[0]
	season = header.split(' ')[0]
	track = header.split(' ')[3]

	data_row += year + "," + season + "," + str(int(track))

	# Get WR time

	divs = html.find_all('div', class_='flex-grow-1')
	wr = str(divs[0].contents[3].contents[0]).strip()
	wr_in_seconds = float(wr.split(':')[0]) * 60 + float(wr.split(':')[1])

	data_row += "," + str(wr_in_seconds)


	# Get medal times
	times = html.find_all('li', class_='my-2')
	times = [str(time.contents[2]).strip() for time in times]

	times_in_seconds = []

	for time in times:
		times_in_seconds.append(float(time.split(':')[0]) * 60 + float(time.split(':')[1]))

	data_row += "," + ",".join([str(time) for time in times_in_seconds])

	# time differences

	gold_to_author = times_in_seconds[1] - times_in_seconds[0]
	author_to_wr = times_in_seconds[0] - wr_in_seconds

	gold_to_author_percent = gold_to_author / times_in_seconds[1]
	author_to_wr_percent = author_to_wr / times_in_seconds[0]

	data_row += "," + str(gold_to_author) + "," + str(author_to_wr) + "," + str(gold_to_author_percent) + "," + str(author_to_wr_percent)

	global data_rows

	data_rows += data_row + "\n"


if __name__ == '__main__':
	getAllTrackLinks(LATEST_CAMPAIGN_URL)
	print(len(all_track_links))
	counter = 0
	for link in all_track_links:
		counter += 1
		print(str(counter) + " / " + str(len(all_track_links)))
		getTrackData(link)
	
	# write data_rows to new file
	with open('trackmania_data.csv', 'w') as f:
		f.write(data_rows)


if __name__ == '__main__!':
	getTrackData("https://www.trackmania.com/tracks/7fsfRSUCQ7YwfBEdRk_GivW6qzj")
	print(data_rows)