## A Python script to download lectures from udemy.com.

### Prerequisites

* Python (2 or 3)
* `pip` (Python Install Packager)
* Python module `requests`
    * If missing, it's automatically installed by `pip`

### Preinstall
If you don't have `pip` installed, look at their [install doc](http://pip.readthedocs.org/en/latest/installing.html).
On Mac it's simple as just running:

    brew install pip

### Install udemy-dl

`udemydl` can be installed using `pip`

    pip install udemydl

or you can clone the repo and install it with `make`

    git clone https://github.com/lestex/udemydl
    cd udemy-dl &&  make all

### Usage

Simply call `udemydl` with the full URL to the course page.

    udemydl https://www.udemy.com/COURSE_NAME

`udemydl` will ask for your udemy username (email address) and password then start downloading the videos.

By default, `udemydl` will create a subdirectory based on the course name (be shure that no traling / sign is uncluded).  If you want to download files to a specific location, use the `-o /path/to/directory/` parameter.

You can include the username/email and password on the command line using the -u and -p parameters.

    udemydl -u user@domain.com -p $ecRe7w0rd https://www.udemy.com/COURSE_NAME

For information about all available parameters, use the `--help` parameter

    udemydl --help

Run in `debug` mode

    udemydl https://www.udemy.com/COURSE_NAME --debug 


### Uninstall

`udemydl` can be uninstalled using `pip`:

    pip uninstall udemydl

or from source code directory with:

    make u
