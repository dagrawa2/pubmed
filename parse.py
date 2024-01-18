import os
import csv
import time
import xml.etree.ElementTree as ET


class CsvDialect(object):
	delimiter = '\t'
	quotechar = '"'
	escapechar = '\\'
	doublequote = False
	skipinitialspace = True
	lineterminator = '\n'
	quoting = csv.QUOTE_ALL


if __name__ == '__main__':

	first_id = 1220
	last_id = 1260
	file_pattern = 'pubmed24n{0:04d}.xml'
	pubmed_dir = 'data'
	out_dir = 'processed'
	os.makedirs(os.path.join(out_dir, 'abstracts'), exist_ok=True)

	for i in range(first_id, last_id):

		fname = file_pattern.format(i)
		fpath = os.path.join(pubmed_dir, fname)
		print('{}: processing {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), fpath))

		tree = ET.parse(fpath)
		root = tree.getroot()

		for pm_article in root.findall('PubmedArticle'):

			medline_citation = pm_article.find('MedlineCitation')
			pubmed_data = pm_article.find('PubmedData')

			if medline_citation is None or pubmed_data is None:
				continue

			pmid = None
			article_id_list = pubmed_data.find('ArticleIdList')
			for article_id in article_id_list.findall('ArticleId'):
				if article_id.attrib['IdType'] == 'pubmed':
					pmid = article_id.text

			article = medline_citation.find('Article')
			title = article.find('ArticleTitle').text

			if title is None:
				continue

			year = None
			for pd in pubmed_data.find('History').findall('PubMedPubDate'):
				if pd.attrib['PubStatus'] == 'pubmed':
					year = pd.find('Year').text
			if not year:
				continue

			language = article.find('Language').text
			if language != 'eng':
				continue

			abstract = article.find('Abstract')
			abstract_text = abstract.find('AbstractText') if abstract is not None else None

			abstract_file = os.path.join(out_dir, 'abstracts', '{}.csv'.format(year))
			with open(abstract_file, 'a') as abstract_fp:
				abstract_writer = csv.writer(abstract_fp, dialect=CsvDialect)
				abstract_writer.writerow([pmid, ' '.join((title, abstract_text.text if abstract_text is not None and abstract_text.text is not None else ''))])
