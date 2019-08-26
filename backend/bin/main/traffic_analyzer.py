import sys

from os import path, environ

if "SPLUNK_HOME" in environ:
    splunk_home = environ["SPLUNK_HOME"]
    sys.path.append(path.join(splunk_home, "etc", "apps", "traffic-analyzer", "bin"))
else:
    sys.path.append(path.join("/opt", "splunk", "etc", "apps", "traffic-analyzer", "bin"))


def convert() -> None:
    import main.convert_pcap as convert_pcap

    print("Start converting")
    convert_pcap.main()


def download() -> None:
    # Readd splunks python2.7 site-packages to sys.path, so that the path is the last element in the path list. Python
    # will follow the order of the list sys.path to check for packages. Because the package reprlib is also located in
    # the splunk specified lib folder, but cannot be used, an ImportError exception with the description 'This package
    # should not be accessible on Python 3.' will be raised.
    splunk_site_packages = path.join("/opt", "splunk", "lib", "python2.7", "site-packages")
    try:
        sys.path.remove(splunk_site_packages)
        sys.path.append(splunk_site_packages)
    except ValueError:
        pass

    import main.downloaders.cipher_downloader as get_ciphers
    import main.downloaders.mac_vendor_downloader as get_mac

    print("Start downloading infos")
    get_ciphers.main()
    get_mac.main()


def enrich() -> None:
    import main.enrich_csv as enrich_csv

    print("Start enriching")
    enrich_csv.main()


def run() -> None:
    convert()
    enrich()


def run_all() -> None:
    download()
    convert()
    enrich()


def main() -> None:
    method = sys.argv[1]

    if method == "convert":
        convert()
    elif method == "download":
        download()
    elif method == "enrich":
        enrich()
    elif method == "run":
        run()
    elif method == "run-all":
        run_all()
    else:
        print(
            "Usage traffic_analyzer.py [option]\n\n"
            "Option:\n"
            "   download:    Download information from IANA and IEEE.\n"
            "   convert:     Converts pcap(ng) files to csv\n"
            "   enrich:      Enriches csvs with additional information\n"
            "   run:         Runs convert and enrich\n"
            "   run-all:     Runs download, convert and enrich"
        )


if __name__ == "__main__":
    main()
