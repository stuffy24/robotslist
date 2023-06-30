from argparse import ArgumentParser
import requests
import sys
from urllib.parse import urljoin


parser = ArgumentParser(
    prog='Robots.txt crawler',
    description='This is a tool that searches a website\'s robots.txt file and then pulls words from those sites.',
    epilog='Make sure to check out Stuffy24 on YOUTUBE!'
)

# Set up help menu
parser.add_argument('-t', "--target", help="Use the syntax -t to specify your target.", required=True)

# Parsing command line arguments
args = parser.parse_args()


def robots_text():
    # This adds /robots.txt to the end of the URL we specified.
    robots_url = urljoin(args.target.rstrip("/"), "robots.txt")

    # Send a GET request to get the contents of the robots.txt file
    response = requests.get(robots_url)

    # Make sure the request was successful
    if response.status_code == 200:
        return response.text
    else:
        return None


def format_urls(disallowed_paths):
    base_url = args.target.rstrip("/")
    formatted_urls = []
    for path in disallowed_paths:
        url = urljoin(base_url, path)
        formatted_urls.append(url)
    return formatted_urls


def main():
    robots_txt = robots_text()
    if robots_txt:
        disallowed_paths = []
        lines = robots_txt.splitlines()
        for line in lines:
            if line.startswith("Disallow:"):
                path = line.split(":", 1)[1].strip()
                disallowed_paths.append(path)
        formatted_urls = format_urls(disallowed_paths)
        for url in formatted_urls:
            print(url)
    else:
        print("Failed to retrieve robots.txt file.")


if __name__ == "__main__":
    main()
