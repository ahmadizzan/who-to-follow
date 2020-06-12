import json
import logging
import time
import twint
import twitter_scraper

from utils import empty_retry

class Profile:

	def __init__(self):
		self.name = None
		self.username = None
		self.birthday = None
		self.bio = None
		self.website = None
		self.profile_photo = None
		self.likes_count = None
		self.tweets_count = None
		self.followers_count = None
		self.following_count = None

	def to_dict(self):
		return {
			'name': self.name,
			'username': self.username,
			'birthday': self.birthday,
			'bio': self.bio.replace('@\n', '@').replace('\n', ' '),
			'website': self.website,
			'profile_photo': self.profile_photo,
			'likes_count': self.likes_count,
			'tweets_count': self.tweets_count,
			'followers_count': self.followers_count,
			'following_count': self.following_count
		}

def generate_follow_graph(root_username, limit=20):
	graph = {}
	graph[root_username] = get_following_list(root_username, limit)
	for username in graph[root_username]:
		graph[username] = get_following_list(username, limit=20)
	return graph

def get_user_profile(username):
	scrape_profile = twitter_scraper.Profile(username)

	profile = Profile()
	profile.name = scrape_profile.name
	profile.username = scrape_profile.username
	profile.birthday = scrape_profile.birthday
	profile.bio = scrape_profile.biography
	profile.website = scrape_profile.website
	profile.profile_photo = scrape_profile.profile_photo
	profile.likes_count = scrape_profile.likes_count
	profile.tweets_count = scrape_profile.tweets_count
	profile.followers_count = scrape_profile.followers_count
	profile.following_count = scrape_profile.following_count

	return profile.to_dict()

@empty_retry(tries=3)
def get_following_list(username, limit=100):
	c = twint.Config()
	c.Username = username
	c.Limit = limit
	c.Store_object = True
	c.Hide_output = True
	c.Debug = False

	twint.output.clean_lists()
	twint.run.Following(c)

	following_list = list(twint.output.follows_list)

	return following_list
