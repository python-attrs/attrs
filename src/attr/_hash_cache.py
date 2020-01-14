import functools
import weakref


# Cache mapping the results of id() to its hash
HASH_CACHE = {}

if getattr(weakref, "finalize", None) is not None:

    def cache_hash(obj, obj_hash):
        global HASH_CACHE
        id_ = id(obj)
        cleanup_cache = functools.partial(HASH_CACHE.pop, id_, None)
        finalizer = weakref.finalize(obj, cleanup_cache)

        # At exit this will clean itself up - these finalizers are just to
        # avoid memory leaks
        finalizer.atexit = False

        # Use `setdefault` for thread-safety
        HASH_CACHE.setdefault(id_, obj_hash)


else:
    _WEAK_REFS = {}

    def _cleanup_weakref(obj_id):
        global HASH_CACHE
        global _WEAK_REFS
        HASH_CACHE.pop(obj_id, None)
        _WEAK_REFS.pop(obj_id, None)

    def cache_hash(obj, obj_hash):
        id_ = id(obj)
        cleanup_cache = functools.partial(_cleanup_weakref, id_)

        r = weakref.ref(obj, cleanup_cache)
        _WEAK_REFS.setdefault(id_, r)
        HASH_CACHE.setdefault(id_, obj_hash)
