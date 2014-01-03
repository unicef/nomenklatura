from pprint import pprint
import dedupe
from itertools import combinations

def entity_to_data(entity):
	data = entity.attributes.copy()
	for key, value in data.items():
		if value is not None:
			value = unicode(value).encode('utf-8')
		data[key] = value
	data['name'] = entity.name.encode('utf-8')
	data['_id'] = entity.id
	data['_canonical_id'] = entity.canonical_id
	return data

def keys_to_fields(keys):
	model = {}
	for key in keys: 
		if key in ['_id', '_canonical_id']:
			continue
		model[key] = {
			'type': 'String',
			'Has Missing': True
		}
	return model

def makeTrainingFunction(num):
	count = [0]
	def canonicalLabel(uncertain_pairs, fields):
		duplicates = []
		nonduplicates = []
		for record_pair in uncertain_pairs:
			l, r = record_pair
			if l.get('_id') == r.get('_canonical_id'):
				duplicates.append(record_pair)
			elif r.get('_id') == l.get('_canonical_id'):
				duplicates.append(record_pair)
			else:
				nonduplicates.append(record_pair)
		count[0] += 1
		return ({0: nonduplicates, 1: duplicates}, count[0]>=num)
	return canonicalLabel

def generate_clusters(dataset):
	print [dataset.name, dataset.entities.count()]
	keys = set()
	entities = []
	for entity in dataset.entities:
		d = entity_to_data(entity)
		keys.update(d.keys())
		entities.append(d)

	for entity in entities:
		for key in keys:
			if not key in entity:
				entity[key] = None
			if entity[key] is None:
				entity[key] = ''

	fields = keys_to_fields(keys)
	deduper = dedupe.Dedupe(fields)

	deduper.train(list(combinations(entities, 2)), makeTrainingFunction(len(entities)/100))

	blocker = deduper.blockingFunction()
	print deduper, blocker

