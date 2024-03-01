import os
import math
import hashlib
from ftplib import FTP
from time import localtime, strftime


def check_hash(dst_path, h):
	file_hash = hashlib.md5(open(dst_path, 'rb').read()).hexdigest()
	return file_hash == h


def check_exists(dst_path, h=None):
	if os.path.exists(dst_path) and os.stat(dst_path).st_size > 0:
		if h is None:
			return True
		if check_hash(dst_path, h):
			return True
	return False


if __name__ == '__main__':
	dst_dir = 'data'
	os.makedirs(dst_dir, exist_ok=True)

	ftp_url = 'ftp.ncbi.nlm.nih.gov'
	ftp_dir = 'pubmed/updatefiles/'

	unsuccessful = []

	total = 0
	successful = 0

	# Connect to FTP server
	ftp = FTP(ftp_url)
	ftp.login()

	# List files to download
	filenames = ftp.nlst(ftp_dir)
	filename_map = {
		filename: None for filename in filenames
		if filename.endswith('.xml.gz')
	}
	for filename in filenames:
		if filename.endswith('.md5'):
			basename = filename.rsplit('.', 1)[0]
			if basename not in filenames:
				print('No matching file for hash: {}'.format(basename))
				continue
			filename_map[basename] = filename

	# Download
	for k, v in filename_map.items():

		file_dst_path = os.path.join(dst_dir, k.rsplit('/', 1)[1])
		hash_dst_path = os.path.join(dst_dir, v.rsplit('/', 1)[1])

		# Get file hash
		if not check_exists(hash_dst_path):
			with open(hash_dst_path, 'wb') as hash_file:
				ftp.retrbinary('RETR '+ v, hash_file.write)
		with open(hash_dst_path, 'r') as hash_file:
			file_hash = hash_file.read().split('=')[1].strip()

		curr_time = strftime("%Y-%m-%d %H:%M:%S", localtime())

		# Download content file
		if not check_exists(file_dst_path, file_hash):
			with open(file_dst_path, 'wb') as local_file:
				ftp.retrbinary('RETR '+ k, local_file.write)

		# Check if downloaded correctly
		if check_hash(file_dst_path, file_hash):
			print('{}: Successfully downloaded file {}'.format(curr_time, k))
			successful += 1
		else:
			print('{}: Error downloading {}'.format(curr_time, k))
			unsuccessful.append(k)
		total += 1

		# Print progress
		if total % math.ceil(float(len(filename_map)) / 100.0) == 0:
			progress = float(total) / float(len(filename_map)) * 100
			print('Progress: %.2f%%' % round(progress, 2))

	print('Successful: {}, total: {}'.format(successful, total))
	print('Unsuccessful IDs:')
	for fid in unsuccessful:
		print(fid)
