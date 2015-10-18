## Synopsis

This is a small python script I made to retrieve some relevant information about tracks I own. I was constantly visiting beatport for the info, so (naturally) I decided to make a python script to do the work for me. My plan is to eventually integrate this tool with my iTunes library so that when new tracks are imported, important information used for mixing is gathered about the track automatically. I wrote this script because I love keeping a clean, accurate music library with all (or most) fields populated.

## Code Example

You can invoke GetTrackDetails.py like this:

```
python GetTrackDetails.py -t "Slingback" -a "A1 Bassline"
```

Example's output:

```
TRACK DETAILS
=============
Title:	Slingback (Original Mix)
Artist:	A1 Bassline
Genre:	Deep House
BPM:	125
```

## Installation

You will need python version 2.7.x and to intall the ['Beautiful Soup'](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) module for python.