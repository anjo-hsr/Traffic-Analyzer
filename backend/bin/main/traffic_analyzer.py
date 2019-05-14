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
