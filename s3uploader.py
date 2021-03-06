#!/usr/bin/python
# -*- coding: utf-8 -*-
#author iamanders.com 
#this is just a test to get the hang of github!

import os
import time
import tarfile
from boto.s3.connection import S3Connection
from boto.s3.key import Key


class uploader:
	"""Class for gzip and upload files to Amazon S3"""
	
	def __init__(self, access_key, secret_key):
		self.access_key = access_key
		self.secret_key = secret_key
		self.s3connection = S3Connection(access_key, secret_key)
	
	def the_magic(self, id, path_to_bup, bucketname, date_in_filename):
		file_contents = os.listdir(path_to_bup)
		if date_in_filename:
			s3_filename = "%s_%s.tar.gz" % (id, time.strftime("%Y-%m-%d-%H%M%S"))
		else:
			s3_filename = id + '.tar.gz'
		temp_filename = '/tmp/backup.tar.gz'
	
		#tar files
		files = os.listdir(path_to_bup)
		tar = tarfile.open(temp_filename, 'w:gz')
		for f in files:
			tar.add(path_to_bup + f)
		tar.close()
	
		#upload
		bucket = self.s3connection.get_bucket(bucketname)
		s3key = Key(bucket)
		s3key.key = s3_filename
		s3key.set_contents_from_filename(temp_filename)



if __name__ == '__main__':
	
	access_key = 'PUT YOUR AMAZON ACCESS KEY HERE!'
	secret_key = 'PUT YOUR AMAZON SECRET KEY HERE!'
	uploader = uploader(access_key, secret_key)

	#To backup
	#you should comment more iamanders :)
	to_backup = [
					{'id': 'foo', 'path': '/path/to/files1/', 'bucket': 'bucket1', 'date': False},
					#{'id': 'bar', 'path': '/path/to/files2/', 'bucket': 'bucket2', 'date': True},
				]
	
	print ''
	
	#Loop and upload
	for b in to_backup:
		print '%s - start backup %s' % (time.strftime("%Y-%m-%d %H:%M:%S"), b['id'])
		try:
			uploader.the_magic(b['id'], b['path'], b['bucket'], b['date'])
		except:
			print '%s - FAIL %s' % (time.strftime("%Y-%m-%d %H:%M:%S"), b['id'])
			
	print ''
	print '%s - DONE!' % time.strftime("%Y-%m-%d %H:%M:%S")
	print ''