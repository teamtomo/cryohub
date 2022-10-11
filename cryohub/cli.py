import click


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
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
@click.version_option()
def cli(paths, name_regex, strict, lazy):
    r"""
    cryohub command line interface.

    Opens files and lands in an interactive ipython shell with data loaded as `data`

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
    if not paths:
        paths = ["./*"]

    from IPython.terminal.embed import InteractiveShellEmbed

    import cryohub

    data = cryohub.read(  # noqa: F841
        *paths,
        name_regex=name_regex,
        strict=strict,
        lazy=lazy,
    )

    # set up ipython shell nicely
    banner = "=== cryohub ==="
    sh = InteractiveShellEmbed(banner2=banner)
    sh.push("data")
    sh()
