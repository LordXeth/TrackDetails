#!/usr/bin/python

# IMPORT MODULES #
import argparse
import urllib2
import json
import re
from bs4 import BeautifulSoup

# PROGRAM CONSTANTS #
g_contentUrl = "https://pro.beatport.com/search"
g_reprog = None

# main method
# program execution begins here
def main():
	progDesc = 'Find the genre of a track from pro.beatport.com. This program works best when you supply both title and artist.'

	parser = argparse.ArgumentParser(description=progDesc)

	parser.add_argument('-t', '--title', nargs='?', help='the title of the track to search for')
	parser.add_argument('-a', '--artist', nargs='?', help='the artist of the track to search for')

	args = parser.parse_args()

	title = ''
	artist = ''

	if (args.title):
		title = args.title
		global g_reprog
		g_reprog = re.compile(r"\b(?=\w)" + re.escape(title) + r"\b(?!\w)")
	if (args.artist):
		artist = args.artist

	searchQueryString = FormatSearchString(artist, title)
	page = GetHtmlContentsAsString(searchQueryString)
	trackData = ParseHtmlPageForJSONData(page)
	trackData.PrintDetails()

# formats the search string used for 
# http GET request to beatport
def FormatSearchString(*searchStringParams):
	queryParts = []
	for string in searchStringParams:
		delimiter = '+'
		splits = [x.strip() for x in string.split()]
		queryPart = delimiter.join(splits)
		queryParts.append(queryPart)

	delimiter = "+"
	searchQueryString = delimiter.join(queryParts)
	return searchQueryString

# returns the html page content as a 
# string from the search request to 
# beatport
def GetHtmlContentsAsString(searchQueryString):
	queryParameter= ("q=" + searchQueryString)
	url = g_contentUrl + "?" + queryParameter
	htmlContent = urllib2.urlopen(url).read()
	return htmlContent

# parses page, receives JSON and creates 
# a track details object that can be reported 
# back to the user
def ParseHtmlPageForJSONData(page):
	soup = BeautifulSoup(page, "html.parser")
	script = soup.find('script', text=re.compile('window\.Playables'))
	json_text = re.search(r'^\s*window\.Playables\s*=\s*({.*?})\s*;\s*$', script.string, flags=re.DOTALL | re.MULTILINE).group(1)
	data = json.loads(json_text)
	tracks = data.get('tracks')

	details = None
	targetTrack = None

	if (len(tracks) > 0):
		for track in tracks:
			match = g_reprog.match(track.get('title'))
			if (match):
				targetTrack = track

		if (targetTrack is None):
			details = TrackDetails('No title found', 'No artist found', 'No genre found', 'No BPM found')
		else:
			title = targetTrack.get('title')
			artists = targetTrack.get('artists')
			artist = artists[0].get('name')
			genres = targetTrack.get('genres')
			genre = genres[0].get('name')
			bpm = str(targetTrack.get('bpm'))
			details = TrackDetails(title, artist, genre, bpm)
	else:
		details = TrackDetails('No title found', 'No artist found', 'No genre found', 'No BPM found')

	return details


# custom track details class
class TrackDetails:

	def __init__(self, title, artist, genre, bpm):
		    self.title = title
		    self.artist = artist
		    self.genre = genre
		    self.bpm = bpm

	def PrintDetails(self):
		print "TRACK DETAILS"
		print "============="
		print "Title:\t" + self.title
		print "Artist:\t" + self.artist
		print "Genre:\t" + self.genre
		print "BPM:\t" + self.bpm

# defines and calls main()
if __name__ == "__main__":
   main()