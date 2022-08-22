import requests, json, os, argparse

# Github: https://github.com/PainDe0Mie/retoken
# Discord: 𝗣ain𝗗e𝟬𝗠ie#4811

with open('config.json') as f:
    data = json.load(f)
    GITHUB_TOKEN = data["GITHUB_TOKEN"]
    GITHUB_USER = data["GITHUB_USER"]
    GITHUB_MAIL = data["GITHUB_MAIL"]

parser = argparse.ArgumentParser()
parser.add_argument("--name", "-n", type=str, dest="name", required=True)
parser.add_argument("--token", "-t", type=str, dest="token", required=True)
parser.add_argument("--private", "-p", dest="is_private", action="store_true")
args = parser.parse_args()
repo_name = args.name
token = args.token
is_private = args.is_private

REPO_PATH = "./"
GITHUB_URL = "https://api.github.com"

if is_private:
    payload = '{"name": "' + repo_name + '", "private": true }'
else:
    payload = '{"name": "' + repo_name + '", "private": false }'

headers = {
    "Authorization": "token " + GITHUB_TOKEN,
    "Accept": "application/vnd.github.v3+json"
}

try:
    r = requests.post(GITHUB_URL + "/user/repos", data=payload, headers=headers)
    r.raise_for_status()
except requests.exceptions.RequestException as err:
    raise SystemExit(err)

try:
    os.chdir(REPO_PATH)
    os.system("mkdir " + repo_name)
    os.chdir(REPO_PATH + repo_name)
    os.system("git init")
    os.system("git remote add origin https://github.com/" + GITHUB_USER + "/" + repo_name + ".git")
    os.system(f"echo '{token}' >> README.md")
    os.system(f'git config --global user.name "{GITHUB_USER}"')
    os.system(f'git config --global user.email "{GITHUB_MAIL}"')
    os.system('git add . && git commit -m "initial commit" && git push origin master')
except FileExistsError as err:
    raise SystemExit(err)
