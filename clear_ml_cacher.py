import time

from allegroai import SingleFrame, DataView
from allegroai.backend_interface import DatasetVersion
import shelve


if __name__ == "__main__":
    tick0 = time.time()
    DatasetVersion._get_default_session()

    tick1 = time.time()

    dataview = DataView("turn_signal_lacking_metadata")

    tick2 = time.time()
    dataview.add_query(
        dataset_id='f60b6b2b0f81412194c8f62b09aa1936',
        version_id='0e5ca95f65874d6f8bd59e093e613f9a',
    )
    tick3 = time.time()
    num_frames = dataview.get_count()

    tick4 = time.time()
    frames = [f for f in dataview.get_iterator(query_cache_size=10000)]

    tick5 = time.time()

    print(f"count: {num_frames}, tick0: {tick1 - tick0}, tick1: {tick2 - tick1}, tick2: {tick3 - tick2}, tick3: {tick4 - tick3}, tick4: {tick5 - tick4}")

    cache = shelve.open(r"I:\Automotive\RnD\noam\cache\uv_data_clearml\atlas_isilon_data\cache")
    for f in frames:
        id_ = f.id
        if id_ not in cache:
            cache[id_] = f

    cache.sync()
    print(f"cache size: {len(cache)}")
