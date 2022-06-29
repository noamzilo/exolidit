import time

from allegroai import Dataset, SingleFrame, DataView
from allegroai.backend_interface import DatasetVersion
import shelve


def main():
    dataview_id = r"40fbb8320ccb4ac98fae490cb10703fc"
    dataview = DataView.get(dataview_id=dataview_id)
    frames = [f for f in dataview]
    frames_with_dataloop_tasks = [f for f in frames if "dataloop_tasks" in f.metadata]
    assert len(frames_with_dataloop_tasks) == len(frames)

    fixed_frames = []
    for f in frames_with_dataloop_tasks:
        del f.metadata["dataloop_tasks"]
        fixed_frames.append(f)
    assert "dataloop_tasks" not in fixed_frames[0].metadata

    dst_dataset_name = "atlas_isilon_all_data"
    dst_version_name = "atlas_all_with_boxes"
    dataset = Dataset.create(dataset_name=dst_dataset_name)
    dataset_version = dataset.get_version(version_name=dst_version_name)
    dataset_version.add_frames(frames, batch_size=10000)

    print(f"Done fixing frames")


if __name__ == "__main__":
    main()
