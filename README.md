## A Python script to download lecture videos for a udemy.com course.

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

`udemy-dl` can be installed using `pip`

    sudo pip install udemy-dl

or you can clone the repo and install it with `make`

    git clone https://github.com/lestex/udemy-dl
    cd udemy-dl &&  make all

### Usage

Simply call `udemy-dl` with the full URL to the course page.

    udemy-dl https://www.udemy.com/COURSE_NAME

`udemy-dl` will ask for your udemy username (email address) and password then start downloading the videos.

By default, `udemy-dl` will create a subdirectory based on the course name (be shure that no traling / sign is uncluded).  If you wish to have the files downloaded to a specific location, use the `-o /path/to/directory/` parameter.

If you wish, you can include the username/email and password on the command line using the -u and -p parameters.

    udemy-dl -u user@domain.com -p $ecRe7w0rd https://www.udemy.com/COURSE_NAME

For information about all available parameters, use the `--help` parameter

    udemy-dl --help

Run in `debug` mode

    udemy-dl https://www.udemy.com/COURSE_NAME --debug 


### Uninstall

`udemy-dl` can be uninstalled using `pip`

    sudo pip uninstall udemy-dl

or

    make u
