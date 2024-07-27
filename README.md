# mock-sccache-plugin

A sccache plugin for mock. That's it.

Currently only supports local caching.

## Installation

You'll need to copy sccache.py into your Mock plugins directory, such as `/usr/lib/python3.12/site-packages/mockbuild/plugins`.

Then within your Mock configuration, you'll have to configure the plugin, for example:

```python
config_opts['plugin_conf']['sccache_enable'] = True
config_opts['plugin_conf']['sccache_opts']['max_cache_size'] = '4G'
config_opts['plugin_conf']['sccache_opts']['compress'] = None
config_opts['plugin_conf']['sccache_opts']['dir'] = "%(cache_topdir)s/%(root)s/sccache/u%(chrootuid)s/"
config_opts['plugin_conf']['sccache_opts']['hashdir'] = True
```

## Credits

The authors of the in-tree mock ccache plugin, which this is highly based on.
