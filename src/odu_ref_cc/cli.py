import click
import shutil


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-s",
    "--select",
    type=int,
    help="Preselect dataset instead of using interactive session",
)
def download_sources(select: int | None = None):
    """
    A cli command that downloads all the data files for a specific challenge.
    Useful if you want to avoid clicking on the files 1 by 1 on the UI.
    """
    from odu_ref_cc import downloader as dl

    click.echo("Getting dataset information...")
    ds = dl.get_datasets()
    try:
        datasets_str = "\n   ".join(
            [
                f"{i} : {dataset_info['title']}"
                for i, dataset_info in enumerate(ds.values())
            ]
        )
        if select is None:
            choice = input(
                "Datasets:\n\n   "
                + datasets_str
                + "\n\n          Which dataset do you want to download? (write the number):  "
            )
            nb_choice = int(choice.strip())
        else:
            nb_choice = select
    except ValueError:
        raise RuntimeError("Please enter an integer as your dataset choice")
    dl.dl_all_resources(list(ds.keys())[nb_choice])


@cli.command()
def clear_downloads():
    """
    delete folder with all ODU CC data
    """
    click.echo("Deleting `data` folder. The contents will be removed.")
    shutil.rmtree("odu-data")
