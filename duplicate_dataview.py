from allegroai import Dataset, DatasetVersion, SingleFrame, DataView


def main():
    src_dataset_id = "f60b6b2b0f81412194c8f62b09aa1936"  # atlas_isilon_data
    src_version_id = "b741753d596042b28323a3d2852e8907"  # turn_signal_with_boxes
    dst_dataset_name = "atlas_isilon_all_data"
    dst_version_name = "atlas_all_with_boxes"

    dataview = DataView("copying_dataview")
    dataview.add_query(
        dataset_id=src_dataset_id,
        version_id=src_version_id
    )

    dataset = Dataset.create(dataset_name=dst_dataset_name)
    dataset_version = DatasetVersion.create_version(
        version_name=dst_version_name,
        dataset_name=dst_dataset_name,
    )
    frames = []
    iterator = dataview.get_iterator(query_cache_size=10000)
    n_frames = len(iterator)
    for i, f in enumerate(iterator):
        print(f"iterating over frame #{i}/{n_frames}: {f.source}")
        frames.append(f)
    dataset_version.add_frames(frames, batch_size=10000)


if __name__ == "__main__":
    main()