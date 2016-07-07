import os
import hashlib
import logging
import pickle
from .cachemanager import CacheManager

l = logging.getLogger("tracer.cachemanager.LocalCacheManager")

class LocalCacheManager(CacheManager):

    def __init__(self, tracer):
        super(LocalCacheManager, self).__init__(tracer)

        binhash = hashlib.md5(open(self.tracer.binary).read()).hexdigest()
        self._cache_file = os.path.join("/tmp", \
                "%s-%s.tcache" % (os.path.basename(self.tracer.binary), binhash))

    def cache_lookup(self):

        if os.path.exists(self._cache_file):
            l.warning("loading state from cache file %s", self._cache_file)

            # just for the testcase
            self.tracer._loaded_from_cache = True

            with open(self._cache_file) as f:
                return pickle.load(f)

    def cacher(self):

        cdata = self._prepare_cache_data()
        if cdata is not None:
            l.warning("caching state to %s", self._cache_file)
            with open(self._cache_file, 'wb') as f:
                f.write(cdata)