import click


@click.group(name="cryohub", context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option()
def cli():
    """
    Cryohub command line interface.
    """
    pass


def _process_extra_kwargs(kwarg_list):
    kwargs_processed = {}
    try:
        for k, v in zip(kwarg_list[::2], kwarg_list[1::2], strict=True):
            if not k.startswith("-"):
                raise click.UsageError(
                    "Only key-value pairs are allowed as extra arguments."
                )

            for typ in (float, int, str):
                try:
                    v = typ(v)
                    break
                except (TypeError, ValueError):
                    continue
                else:
                    raise TypeError('could not convert "{v}" to a usable type')
            kwargs_processed[k.strip("-").replace("-", "_")] = v
    except ValueError:
        raise click.UsageError("Only key-value pairs are allowed as extra arguments.")
    return kwargs_processed


@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("input", type=click.Path(exists=True, dir_okay=True, resolve_path=True))
@click.argument("output", type=click.Path(dir_okay=False, resolve_path=True))
@click.option(
    "-n",
    "--name-regex",
    metavar="regex",
    help=r"a regex used to infer DataBlock names from paths [fallback: \d+]",
)
@click.option(
    "-f", "--overwrite", is_flag=True, help="Overwrite existing output files."
)
@click.argument("kwargs", nargs=-1, type=click.UNPROCESSED)
def convert(input, output, name_regex, overwrite, kwargs):
    """Convert files between available formats."""
    from pathlib import Path

    import cryohub

    output = Path(output)
    if output.exists() and not overwrite:
        raise click.UsageError(f"{output} already exists. Use -f to overwrite.")

    data = cryohub.read(  # noqa: F841
        input,
        name_regex=name_regex,
        **_process_extra_kwargs(kwargs),
    )
    cryohub.write(data, output, overwrite=overwrite)


@cli.command()
@click.argument("paths", nargs=-1)
@click.option(
    "-n",
    "--name-regex",
    metavar="regex",
    help=r"a regex used to infer DataBlock names from paths [fallback: \d+]",
)
@click.option(
    "--strict", is_flag=True, help="immediately fail if a matched path cannot be read"
)
@click.option(
    "--lazy", is_flag=True, default=True, help="read data lazily (if possible)"
)
def view(paths, name_regex, strict, lazy):
    r"""
    Open files and land in an interactive ipython shell.

    Loaded data is stored in the `data` variable.

    PATHS: any number of files [default='.']

    EXAMPLES:

    Open a .star file as particles:

        cryohub particles.star

    Open particles and images from a directory:

        cryohub /dir/with/star_and_mrc_files/

    Match files such as MyProtein_10.star and MyProtein_001.mrc,
    and name the respective data objects Protein_10 and Protein_001:

        cryohub /path/to/dir/MyProtein* -n 'Protein_\d+'
    """
    from inspect import cleandoc

    from IPython.terminal.embed import InteractiveShellEmbed

    import cryohub

    if not paths:
        paths = ["./*"]

    data = cryohub.read(  # noqa: F841
        *paths,
        name_regex=name_regex,
        strict=strict,
        lazy=lazy,
    )

    # set up ipython shell nicely
    banner = """
        === cryohub ===
        - loaded data is in the list `data`
    """
    # sh.instance() needed due to reggression in ipython
    # https://github.com/ipython/ipython/issues/13966#issuecomment-1696137868
    sh = InteractiveShellEmbed.instance(banner2=cleandoc(banner))
    sh()
