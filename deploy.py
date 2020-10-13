#!/usr/bin/python3

import requests, click, json
from os import environ


@click.group()
def cli():
    pass

@click.command()
def show():
    print("===checking the deployments===")
    headers = {"Authorization": f"token {environ['ghkey']}"}
    r = requests.get("https://api.github.com/repos/roylarsen/card_collection/deployments", headers=headers)
    
    if r.status_code != 200:
        print("Error!")
        print(f"{r.status_code} - {r.text}")
        exit(1)

    print("Registered Deployments")
    print(f"{r.json()}")

@click.command()
@click.option('--env', help='Deployment Environment')
def create(env):
    print("===creating the deployment===")
    headers = {"Authorization": f"token {environ['ghkey']}", "Accept": "application/vnd.github.v3+json"}
    payload = {
        'ref': 'master',
        'environment': env,
        'required_contexts': [],
        "payload": {
          "deploy": "prod"
        },
        "description": "dumb python deploy script"
    }

    r = requests.post("https://api.github.com/repos/roylarsen/card_collection/deployments", headers=headers, data=json.dumps(payload))

    if r.status_code not in range(200, 299):
        print("Error!")
        print(f"{r.status_code} - {r.text}")
        exit(1)
    
    print(r.json())

@click.command()
@click.option('--id', help='Deployment to Delete')
def delete(id):
    print("===deleting the deployment===")
    headers = {"Authorization": f"token {environ['ghkey']}", "Accept": "application/vnd.github.v3+json"}

    r = requests.delete(f"https://api.github.com/repos/roylarsen/card_collection/deployments/{id}", headers=headers)

    if r.status_code not in range(200, 299):
        print("Error!")
        print(f"{r.status_code} - {r.text}")
        exit(1)
    
    print(r.text)

cli.add_command(show)
cli.add_command(create)
cli.add_command(delete)

if __name__ == "__main__":
    if "ghkey" not in environ:
        print("Set ghkey in environment")
        exit(1)
    cli()