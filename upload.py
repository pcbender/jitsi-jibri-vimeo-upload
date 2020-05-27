#!/usr/bin/python3

import json
import os
import vimeo
import sys
import fnmatch
from urllib.parse import urlparse
from datetime import datetime
import re

def upload(file_name):
	
	recording_path = os.path.dirname(file_name)
	
	metadata_file = os.path.join(recording_path, 'metadata.json')
	
	metadata = json.load(open(metadata_file))
	
	parsed = urlparse(metadata['meeting_url'])
	
	meeting_name = re.sub('[^a-zA-Z0-9]', ' ', parsed.path).title()
	host_name = parsed.hostname
	
	print(('Begin uploading: %s ...' % file_name))
	
	create_date = datetime.now().strftime('%m-%d-%y')
	
	try:
		# Upload the file and include the video title and description.
		uri = client.upload(file_name, data={
			'name': meeting_name + ' - ' + create_date,
			'description': "This video was uploaded from " + host_name + '.'
		})
		print(('%s has been uploaded to %s' % (file_name, uri)))
		return True
	except vimeo.exceptions.UploadAttemptCreationFailure as e1:
		# We may have had an error. We can't resolve it here necessarily, so
		# report it to the user.
		print(('\tError uploading %s' % file_name))
		print(('\tServer reported: %s' % e1.message))
		return False
	except vimeo.exceptions.VideoUploadFailure as e:
		# We may have had an error. We can't resolve it here necessarily, so
		# report it to the user.
		print(('\tError uploading %s' % file_name))
		print(('\tServer reported: %s' % e.message))
		return False
	except:
		print(('\tUnexpected error: %s' % sys.exc_info()[0]))
		return False

def delete(file_name):
	recording_path = os.path.dirname(file_name)
	print(('Deleting: %s' % recording_path))
	os.system('rm -r ' + recording_path)

config_file = os.path.dirname(os.path.realpath(__file__)) + '/upload.config.json'
config = json.load(open(config_file))

if 'client_id' not in config or 'client_secret' not in config:
    raise Exception('We could not locate your client id or client secret ' +
                    'in `' + config_file + '`. Please create one, and ' +
                    'reference `upload.config.json`.')

sys.stdout = open(config["log_file"], "a+")

print(('\nStart: %s' % datetime.now()))

# Instantiate the library with your client id, secret and access token
# (pulled from the vimeo dev site)
client = vimeo.VimeoClient(
    token=config['access_token'],
    key=config['client_id'],
    secret=config['client_secret']
)

if len(sys.argv) != 2:
	raise Exception('The file information argument was not passed to this script by the caller.')

dir_name = sys.argv[1]

dir_path = os.path.dirname(dir_name)

matches = []

try:
	for root, dirnames, filenames in os.walk(dir_path):
		for filename in fnmatch.filter(filenames, '*.mp4'):
			matches.append(os.path.join(root, filename))

	for filename in matches:
		if upload(filename):
			delete(filename)

finally:
	print(('End: %s \n' % datetime.now()))
	sys.stdout.close()

