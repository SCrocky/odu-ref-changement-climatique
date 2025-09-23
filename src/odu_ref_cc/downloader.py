import httpx
import os
from tqdm import tqdm

from odu_ref_cc.log import log

API_SCHEMA = {
    "challenge_name": "changement-climatique",
    "url": "https://www.data.gouv.fr/api/2",
    "endpoints": {
        "topic": "topics/changement-climatique/",
        "datasets": "datasets/{dataset_id}/",
        "resources": "datasets/{dataset_id}/resources/",
    },
}


def get_datasets():
    res = httpx.get("/".join([API_SCHEMA["url"], API_SCHEMA["endpoints"]["topic"]]))
    res.raise_for_status()
    return {
        ds_info["id"]: get_dataset_info(ds_info["id"])
        for ds_info in res.json()["extras"]["defis"]["datasets_properties"]
    }


def get_dataset_info(dataset_id: str):
    endpoint = API_SCHEMA["endpoints"]["datasets"].format(dataset_id=dataset_id)
    res = httpx.get("/".join([API_SCHEMA["url"], endpoint]))
    res.raise_for_status()
    return res.json()


def get_resources(
    dataset_id: None | str = None,
    **extra_params,
):
    client = httpx.Client()
    url = API_SCHEMA["url"]
    endpoint = API_SCHEMA["endpoints"]["resources"].format(dataset_id=dataset_id)
    page = 1
    res = client.get(
        f"{url}/{endpoint}",
        params={"page": page, "page_size": 100, **extra_params},
    )
    data = res.json()["data"]
    while len(data) < res.json()["total"]:
        page += 1
        res = client.get(
            f"{url}/{endpoint}",
            params={"page": page, "page_size": 100, **extra_params},
        )
        data.extend(res.json()["data"])
    res.raise_for_status()
    return data


def dl_resource(resource: dict, title: str):
    filepath = f'data/{title}/{resource["title"]}'
    if not filepath.endswith(resource["format"]):
        filepath += f'.{resource["format"]}'
    if not filepath.endswith("csv.gz"):
        log.info(f"Skipping file {filepath} as it doesn't seem to be a data file")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    log.info(f"Downloading file to: {filepath}")
    with open(filepath, "wb") as writer:
        with httpx.stream("GET", resource["url"]) as res:
            res.raise_for_status()
            num_bytes_downloaded = res.num_bytes_downloaded
            with tqdm(
                total=resource["filesize"], unit_scale=True, unit_divisor=1024, unit="B"
            ) as progress:
                for chunk in res.iter_bytes():
                    writer.write(chunk)
                    progress.update(res.num_bytes_downloaded - num_bytes_downloaded)
                    num_bytes_downloaded = res.num_bytes_downloaded


def dl_all_resources(dataset: str):
    title = get_dataset_info(dataset)["title"]
    for resource in get_resources(dataset):
        dl_resource(resource=resource, title=title)
