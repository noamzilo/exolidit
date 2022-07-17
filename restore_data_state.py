from allegroai import Dataset, SingleFrame, DataView
import dtlpy as dl


def is_last_dataloop_task_in_clearml(
        dl_project,
):
    """
    Check the last batch of data loop is fully reflected in ClearML
    TODO check the other way around
    """
    datasets = dl_project.datasets.list()
    if len(datasets) == 0:
        return True  # empty case of "all datasets are reflected in ClearML"
    last_dataset = datasets[-1]  # This assumes errors may only occur last TODO Did not think of all use-cases.
    last_dataset_items = last_dataset.items.list().items

    if len(last_dataset_items) == 0:
        return False  # there shouldn't exist an empty dataset in Dataloop
    clearml_frame_ids = []
    clearml_dataset_ids = []
    clearml_version_ids = []
    dataloop_item_ids = set()
    for item in last_dataset_items:
        metadata = item.metadata
        clearml_metadata = metadata["clearml_origin"]
        clearml_frame_ids.append(clearml_metadata["frame_id"])
        clearml_dataset_ids.append(clearml_metadata["dataset_id"])
        clearml_version_ids.append(clearml_metadata["version_id"])
        dataloop_item_ids.add(item.id)

    # TODO assuming all frames originate from the same dataset/dataset version in ClearML | wrong assumption
    # TODO make smarter queries based on several versions/datasets
    first_frame_dataset, first_frame_dataset_version = clearml_dataset_ids[0], clearml_version_ids[0]
    query_string = ' OR '.join([f"id: {id_}" for id_ in clearml_frame_ids])

    dataview = DataView()
    dataview.add_query(
        dataset_id=first_frame_dataset,
        version_id=first_frame_dataset_version,
        frame_query=query_string
    )

    allegro_frames = [f for f in dataview]
    if len(allegro_frames) != len(last_dataset_items):
        return False

    # validate all ClearML frames have been marked for this dataloop task
    for allegro_frame in allegro_frames:
        meta = allegro_frame.metadata
        if "dataloop_tasks" not in meta:
            return False

        # TODO this part is untested.
        dl_tasks = meta["dataloop_tasks"]
        for task in dl_tasks:
            item_id = task["item_id"]
            if item_id in dataloop_item_ids:
                break
        else:
            return False

    return True


def delete_last_dataset_from_dataloop_project(dl_project):
    """
    delete the last dataset. TODO think if this is enough, and consider respectively updating ClearML instead
    """
    # TODO these credentials are duplicated everywhere, inject them

    email, password = r"bot.388e15cc-12e7-43c5-9987-19c10d9233df@bot.dataloop.ai", r"74MO*1ib6^280qQ^z"
    if dl.token_expired():
        assert dl.login_m2m(email=email, password=password)

    print(f"deleting last dataset from dataloop project: {dl_project.name}")
    # delete the last dataset from the project.
    datasets = dl_project.datasets.list()
    last_dataset = datasets[-1]
    assert last_dataset.name == "batch_018"
    # TODO catch errors from the deleting API call
    dl_project.datasets.delete(dataset_id=last_dataset.id)
    # need more stuff?


def remove_dataloop_from_dataview_in_clearml(dataview_id):
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


def main():
    dl_project_name = "noam_test"
    dl_project = dl.projects.get(dl_project_name)
    if not is_last_dataloop_task_in_clearml(dl_project):
        delete_last_dataset_from_dataloop_project(dl_project=dl_project)


if __name__ == "__main__":
    main()
