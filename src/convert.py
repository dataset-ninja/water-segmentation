import supervisely as sly
import numpy as np
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, file_exists
import shutil

from tqdm import tqdm

def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    images_path = os.path.join("water_v2","water_v2","JPEGImages")
    masks_path = os.path.join("water_v2","water_v2","Annotations")
    train_split_path = os.path.join("water_v2","water_v2","train.txt")
    val_split_path = os.path.join("water_v2","water_v2","val.txt")
    masks_ext = ".png"

    blank_masks = [
        "water_v2\water_v2\Annotations\ADE20K\ADE_train_00002842.png",
        "water_v2\water_v2\Annotations\ADE20K\ADE_train_00003321.png",
        "water_v2\water_v2\Annotations\ADE20K\ADE_train_00004994.png",
        "water_v2\water_v2\Annotations\ADE20K\ADE_train_00009491.png",
        "water_v2\water_v2\Annotations\ADE20K\ADE_train_00009944.png",
        "water_v2\water_v2\Annotations\ADE20K\ADE_train_00011570.png",
        "water_v2\water_v2\Annotations\ADE20K\ADE_train_00014491.png",
        "water_v2\water_v2\Annotations\ADE20K\ADE_train_00019048.png",
    ]

    batch_size = 30


    def create_ann(image_path):
        labels = []

        image_name = get_file_name(image_path)
        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        mask_path = os.path.join(masks_path, folder, image_name + masks_ext)
        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            uniq = np.unique(mask_np)
            if len(uniq)>1:
                mask = mask_np == 255
                curr_bitmap = sly.Bitmap(mask)
                curr_label = sly.Label(curr_bitmap, obj_class)
                labels.append(curr_label)

        tag = sly.Tag(meta=tag_seq,value=folder)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=[tag])

    tag_seq = sly.TagMeta(name="seq", value_type=sly.TagValueType.ANY_STRING)
    obj_class = sly.ObjClass("water", sly.Bitmap)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[obj_class],tag_metas=[tag_seq])


    train_folders = []
    with open(train_split_path) as f:
        content = f.read().split("\n")
        for curr_data in content:
            if len(curr_data) > 0:
                train_folders.append(curr_data)
                tag_meta = sly.TagMeta(curr_data, sly.TagValueType.NONE)
                meta = meta.add_tag_meta(tag_meta)

    val_folders = []
    with open(val_split_path) as f:
        content = f.read().split("\n")
        for curr_data in content:
            if len(curr_data) > 0:
                val_folders.append(curr_data)
                tag_meta = sly.TagMeta(curr_data, sly.TagValueType.NONE)
                meta = meta.add_tag_meta(tag_meta)


    api.project.update_meta(project.id, meta.to_json())

    ds_name_to_folders = {"train": train_folders, "val": val_folders}

    for ds_name, folders in ds_name_to_folders.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        for folder in folders:
            curr_images_path = os.path.join(images_path, folder)
            images_names = os.listdir(curr_images_path)
            progress = sly.Progress(
                "Create dataset {}, add {} data".format(ds_name, folder), len(images_names)
            )

            for img_names_batch in sly.batched(images_names, batch_size=batch_size):
                images_pathes_batch = [
                    os.path.join(curr_images_path, image_name) for image_name in img_names_batch
                ]

                new_images_names = [folder.split("_")[0] + "_" + im_name for im_name in img_names_batch]

                img_infos = api.image.upload_paths(dataset.id, new_images_names, images_pathes_batch)
                img_ids = [im_info.id for im_info in img_infos]

                anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
                api.annotation.upload_anns(img_ids, anns_batch)

                progress.iters_done_report(len(img_names_batch))

    return project
