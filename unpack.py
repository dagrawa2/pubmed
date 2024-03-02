import os
import gzip

if __name__ == '__main__':
	metadata_dir = 'data'

	filenames = os.listdir(metadata_dir)
	total = sum([1 for filename in filenames if filename.endswith('.xml.gz')])
	processed = 0

	for filename in filenames:
		if filename.endswith('.xml.gz'):
			filepath = os.path.join(metadata_dir, filename)
			outpath = filepath.rsplit('.', 1)[0]
			with gzip.open(filepath, 'rb') as archive, open(outpath, 'wb') as fp:
				fp.write(archive.read())
				processed += 1
			print('{}/{} complete \r'.format(processed, total))
