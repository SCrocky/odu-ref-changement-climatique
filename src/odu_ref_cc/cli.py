import click


@click.group()
def cli():
    pass


@cli.command()
def download_sources():
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
        choice = input(
            "Datasets:\n\n   "
            + datasets_str
            + "\n\n          Which dataset do you want to download? (write the number):  "
        )
        nb_choice = int(choice.strip())
    except ValueError:
        raise RuntimeError("Please enter an integer as your dataset choice")
    dl.dl_all_resources(list(ds.keys())[nb_choice])


@cli.command()
def clear_downloads():
    click.echo("Dropped the database")
