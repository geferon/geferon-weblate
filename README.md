
Python module for parsing and saving Valve VDF translation files for Weblate.
This module hasn't been fully tested, so it might receive future updates to fix issues which are currently unknown to me.

# Installing

To install, you will have to either clone this repo and do a `git install -e FOLDER` over the repository, or install it directly via

```
pip install git+https://github.com/geferon/geferon-weblate
```

## Adding to settings.py

Once you installed the Python module, to add the VDF Language Translation, you will have to add the custom format to the setting `WEBLATE_FORMATS` inside of settings.py

The line you'll have to add is:
```python
	'geferon.weblate.formats.VdfFormat'
```

This would result in:
```python
WEBLATE_FORMATS = (
	# etc
	'geferon.weblate.formats.VdfFormat'
)
```

By default the file settings.py doesn't come with the setting `WEBLATE_FORMATS`, so you'll have to include it with all the default formats.
This would result in (VDF Format included):

```python
WEBLATE_FORMATS = (
    'weblate.formats.ttkit.PoFormat',
    'weblate.formats.ttkit.PoMonoFormat',
    'weblate.formats.ttkit.TSFormat',
    'weblate.formats.ttkit.XliffFormat',
    'weblate.formats.ttkit.PoXliffFormat',
    'weblate.formats.ttkit.StringsFormat',
    'weblate.formats.ttkit.StringsUtf8Format',
    'weblate.formats.ttkit.PropertiesUtf8Format',
    'weblate.formats.ttkit.PropertiesUtf16Format',
    'weblate.formats.ttkit.PropertiesFormat',
    'weblate.formats.ttkit.JoomlaFormat',
    'weblate.formats.ttkit.PhpFormat',
    'weblate.formats.ttkit.RESXFormat',
    'weblate.formats.ttkit.AndroidFormat',
    'weblate.formats.ttkit.JSONFormat',
    'weblate.formats.ttkit.JSONNestedFormat',
    'weblate.formats.ttkit.WebExtensionJSONFormat',
    'weblate.formats.ttkit.I18NextFormat',
    'weblate.formats.ttkit.CSVFormat',
    'weblate.formats.ttkit.CSVSimpleFormat',
    'weblate.formats.ttkit.CSVSimpleFormatISO',
    'weblate.formats.ttkit.YAMLFormat',
    'weblate.formats.ttkit.RubyYAMLFormat',
    'weblate.formats.ttkit.SubRipFormat',
    'weblate.formats.ttkit.MicroDVDFormat',
    'weblate.formats.ttkit.AdvSubStationAlphaFormat',
    'weblate.formats.ttkit.SubStationAlphaFormat',
    'weblate.formats.ttkit.DTDFormat',
    'weblate.formats.ttkit.WindowsRCFormat',
    'weblate.formats.ttkit.FlatXMLFormat',
    'weblate.formats.external.XlsxFormat',
    'weblate.formats.txt.AppStoreFormat',
    'geferon.weblate.formats.VdfFormat'
)
```

# Problems

* It is known that sometimes when parsing files that have no quotes to define keys, which have dots or some other special characters, can result in the parser identifying wrong keys. This is due to the vdf package dependency that this module uses, which I fixed by forking the original https://github.com/geferon/vdf

   In the dependencies of this package, it has been specified to use the fork instead of the original, but due to how Python dependencies work, if you have the original installed, it will not download mine. This can be fixed by uninstalling the original and installing this module again, or by installing my fork manually via `pip install git+https://github.com/geferon/vdf.git`

