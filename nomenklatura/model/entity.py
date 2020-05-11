from datetime import datetime

from formencode import All, FancyValidator, Invalid, Schema, validators
from normality import normalize
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.orm import backref, joinedload_all
from werkzeug.exceptions import NotFound

from nomenklatura.core import db


class EntityState():

    def __init__(self, dataset, entity):
        self.dataset = dataset
        self.entity = entity


class AvailableName(FancyValidator):

    def _to_python(self, name, state):
        entity = Entity.by_name(state.dataset, name)
        if entity is None:
            return name
        if state.entity and entity.id == state.entity.id:
            return name
        raise Invalid('Entity already exists.', name, None)


class ValidCanonicalEntity(FancyValidator):

    def _to_python(self, value, state):
        if isinstance(value, dict):
            value = value.get('id')
        entity = Entity.by_id(value)
        if entity is None:
            entity = Entity.by_name(state.dataset, value)
        if entity is None:
            raise Invalid('Entity does not exist: %s' % value, value, None)
        if entity == state.entity:
            return None
        if entity.dataset != state.dataset:
            raise Invalid('Entity belongs to a different dataset.',
                          value, None)
        return entity


class AttributeSchema(Schema):
    allow_extra_fields = True


class EntitySchema(Schema):
    allow_extra_fields = True
    name = All(validators.String(min=0, max=5000), AvailableName())
    attributes = AttributeSchema()
    reviewed = validators.StringBool(if_empty=False, if_missing=False)
    invalid = validators.StringBool(if_empty=False, if_missing=False)
    canonical = ValidCanonicalEntity(if_missing=None, if_empty=None)


class Entity(db.Model):
    __tablename__ = 'entity'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    normalized = db.Column(db.Unicode)
    attributes = db.Column(HSTORE)
    reviewed = db.Column(db.Boolean, default=False)
    invalid = db.Column(db.Boolean, default=False)
    canonical_id = db.Column(db.Integer,
                             db.ForeignKey('entity.id'), nullable=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    canonical = db.relationship('Entity', remote_side='Entity.id',
                                backref=backref('aliases', lazy='dynamic'))

    def to_dict(self, shallow=False):
        d = {
            'id': self.id,
            'name': self.name,
            'dataset': self.dataset.name,
            'reviewed': self.reviewed,
            'invalid': self.invalid,
            'canonical': self.canonical,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        if not shallow:
            d['creator'] = self.creator.to_dict()
            d['attributes'] = self.attributes
            d['num_aliases'] = self.aliases.count()
        return d

    def to_row(self):
        row = self.attributes or {}
        row = row.copy()
        row.update(self.to_dict(shallow=True))
        if self.canonical is not None:
            row['canonical'] = self.canonical.name
        return row

    @property
    def display_name(self):
        return self.name

    @classmethod
    def by_name(cls, dataset, name):
        q = cls.query.filter_by(dataset=dataset)
        attr = Entity.name
        if dataset.normalize_text:
            attr = Entity.normalized
            name = normalize(name)
        if dataset.ignore_case:
            attr = func.lower(attr)
            if isinstance(name, str):
                name = name.lower()
        q = q.filter(attr == name)
        return q.first()

    @classmethod
    def by_id(cls, id):
        try:
            return cls.query.filter_by(id=int(id)).first()
        except ValueError:
            return None

    @classmethod
    def id_map(cls, ids):
        entities = {}
        for entity in cls.query.filter(cls.id.in_(ids)):
            entities[entity.id] = entity
        return entities

    @classmethod
    def find(cls, dataset, id):
        entity = cls.by_id(id)
        if entity is None:
            raise NotFound("No such value ID: %s" % id)
        return entity

    @classmethod
    def all(cls, dataset=None, query=None, eager_aliases=False, eager=False):
        q = cls.query
        if dataset is not None:
            q = q.filter_by(dataset=dataset)
        if query is not None and len(query.strip()):
            q = q.filter(cls.name.ilike('%%%s%%' % query.strip()))
        if eager_aliases:
            q = q.options(joinedload_all(cls.aliases_static))
        if eager:
            q = q.options(db.joinedload('dataset'))
            q = q.options(db.joinedload('creator'))
        return q

    @classmethod
    def create(cls, dataset, data, account):
        state = EntityState(dataset, None)
        data = EntitySchema().to_python(data, state)
        entity = cls()
        entity.dataset = dataset
        entity.creator = account
        entity.name = data['name']
        entity.normalized = normalize(entity.name)
        entity.attributes = data.get('attributes', {})
        entity.reviewed = data['reviewed']
        entity.invalid = data['invalid']
        entity.canonical = data['canonical']
        db.session.add(entity)
        db.session.flush()
        return entity

    def update(self, data, account):
        state = EntityState(self.dataset, self)
        data = EntitySchema().to_python(data, state)
        self.creator = account
        self.name = data['name']
        self.normalized = normalize(self.name)
        self.attributes = data['attributes']
        self.reviewed = data['reviewed']
        self.invalid = data['invalid']
        self.canonical = data['canonical']

        # redirect all aliases of this entity
        if self.canonical:
            if self.canonical.canonical_id:
                if self.canonial.canonical_id == self.id:
                    self.canonical.canonical = None
                else:
                    self.canonical = self.canonical.canonical

            for alias in self.aliases:
                alias.canonical = self.canonical

        db.session.add(self)
