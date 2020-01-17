import six
import os
import tempfile
import copy
import vdf
import pycountry
import chardet
import codecs
import io

from itertools import chain

from django.apps import AppConfig

from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from weblate.formats.base import TranslationFormat, TranslationUnit, move_atomic
from weblate.utils.errors import report_error


class VDFUnit(TranslationUnit):
    @cached_property
    def locations(self):
        return ''

    @cached_property
    def source(self):
        if self.template is not None:
            return self.template.text
        return self.unit.text

    @cached_property
    def target(self):
        if self.unit is None:
            return ''
        return self.unit.text

    @cached_property
    def context(self):
        return self.mainunit.key

    def set_target(self, target):
        self._invalidate_target()
        self.unit.text = target

    def mark_fuzzy(self, fuzzy):
        return

    def mark_approved(self, value):
        return

class VDFItem(object):
    def __init__(self, key, text):
        self.key = key
        self.text = text

    @cached_property
    def location(self):
        return '{}'.format(self.key)

    def getid(self):
        return self.key

defaultCodec = 'UTF-16-LE'

vdfTranslationBase = vdf.VDFDict()
vdfTranslationBase['lang'] = vdf.VDFDict()
vdfTranslationBase['lang']['Language'] = 'English' # TODO
vdfTranslationBase['lang']['Tokens'] = vdf.VDFDict()

class VDFSerializer(object):
    def __init__(self, units, language):
        self.units = units
        self.language = language
    
    def __call__(self, handle):
        # language = pycountry.languages.get(alpha_2=self.language)

        # file_base = copy.deepcopy(vdfTranslationBase)
        file_base = vdf.loads(vdf.dumps(vdfTranslationBase)) # copy structure
        # file_base['lang']['Language'] = language.name
        file_base['lang']['Language'] = self.language.capitalize()

        for unit in self.units:
            file_base['lang']['Tokens'][unit.key] = unit.text

        file_content = vdf.dump(file_base, handle, pretty=True)


class VDFParser(object):
    codec = defaultCodec

    def __init__(self, storefile):
        if not isinstance(storefile, six.string_types):
            raise ValueError('Needs string as a storefile!')

        self.base = storefile

        with open(storefile, 'rb') as handle:
            rawdata = handle.read()

            # First let's try the default codec, which is the normally supported by Valve games
            try:
                self.content = rawdata.decode(defaultCodec)
            except: # if it fails, let's find out what codec it has
                result = chardet.detect(rawdata)
                self.codec = result['encoding']
                if self.codec.lower() == 'ascii': # If it's ascii, convert automatically to UTF-8, as UTF-8 is completely valid for ASCII
                    self.codec = 'utf-8'
                self.content = rawdata.decode(self.codec)

            self.parsed = vdf.parse(io.StringIO(self.content))

        self.units = list(
            VDFItem(itemKey, itemValue) for itemKey, itemValue in self.parsed['lang']['Tokens'].items()
        )



class VdfFormat(TranslationFormat):
    name = _('Valve VDF Translation Files')
    format_id = 'valvevdf'
    monolingual = True
    autoload = ('*_*.txt',)
    unit_class = VDFUnit
    new_translation = vdfTranslationBase
    language_format = "full"

    def __init__(self, storefile, template_store=None, language_code=None, is_template=False):
        super(VdfFormat, self).__init__(
            storefile, template_store, language_code, is_template
        )
        self.language_code = language_code

    @classmethod
    def get_language_full(cls, code):
        lng_code = cls.get_language_code(code, 'posix')
        language = pycountry.languages.get(alpha_2=lng_code).name.lower()
        return language

    # @classmethod
    # def get_language_filename(cls, mask, code):
    #     mask.replace('*', '*_' + cls.get_language_full(code))

    @classmethod
    def load(cls, storefile):
        return VDFParser(storefile)

    def save_content(self, handle):
        vdf.dump(self.store, handle, pretty=True)

    def save(self):
        self.save_atomic(
            self.storefile,
            VDFSerializer(self.store.units, self.language_code)
        )
    
    def save_atomic(self, filename, callback):
        dirname, basename = os.path.split(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        temp = tempfile.NamedTemporaryFile(
            mode='w', prefix=basename, dir=dirname, delete=False, encoding=self.store.codec
        )
        try:
            callback(temp)
            temp.close()
            move_atomic(temp.name, filename)
        finally:
            if os.path.exists(temp.name):
                os.unlink(temp.name)


    def is_valid(self):
        if self.store is None or self.store.parsed is None:
            return False

        return True

    def add_unit(self, unit):
        self.store.units.append(unit)

    def create_unit(self, key, source):
        unit = VDFItem(key, source)
        return unit

    @classmethod
    def get_new_file_content(cls):
        sample_text = vdf.dumps(cls.new_translation, pretty=True)
        sample_bytes = codecs.encode(sample_text, defaultCodec)
        return sample_bytes

    @classmethod
    def create_new_file(cls, filename, language, base):
        if base:
            store = cls.load(base)
            cls.untranslate_store(store, language)
        elif cls.new_translation is None:
            raise ValueError('Not supported')
        else:
            store = cls.load(vdf.dumps(cls.new_translation)) # Copy translation obj

        with codecs.open(filename, 'w', store.codec if base else defaultCodec) as handle:
            # vdf.dump(store, handle, pretty=True)
            VDFSerializer(store.units, language)(handle)

    @classmethod
    def is_valid_base_for_new(cls, base, monolingual):
        if not base:
            return monolingual and cls.new_translation is not None
        try:
            cls.load(base)
            return True
        except Exception as error:
            report_error(error, prefix='File parse error')
            return False

    @classmethod
    def untranslate_store(cls, store, language):
        for unit in store.units:
            unit.text = ''


    @classmethod
    def get_class(cls):
        return None

# class FormatsConfig(AppConfig):
#     name = 'geferon'
#     verbose_name = "Geferon Custom Formats"
