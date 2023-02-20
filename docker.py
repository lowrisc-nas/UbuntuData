import subprocess
import json

from datetime import datetime, timedelta

def docker_containers(all: bool=False) -> list[str]:
  """Get a list of the docker containers by name

  Args:
      all (bool, optional): If true returns active and idle containers.
        Otherwise just returns active containers. Defaults to False.

  Returns:
      list[str]: List of container names
  """
  dformat = "{{.Names}}"
  if all:
    return subprocess.check_output(['docker', 'ps', '-a', '--format', dformat]).decode('utf-8').split("\n")
  else:
    return subprocess.check_output(['docker', 'ps', '--format', dformat]).decode('utf-8').split("\n")


def docker_status(name: str) -> dict:
  try:
    inspect = subprocess.check_output(['docker', 'container', 'inspect', name]).decode('utf-8')
  except subprocess.CalledProcessError as e:
    return None

  status = json.loads(inspect)

  if len(status) < 1:
    return None

  return status[0]


def docker_uptime(name: str) -> timedelta:
  status = docker_status(name)

  if status is None:
    return -1

  start = datetime.strptime(
    status["State"]["FinishedAt"][:-4],
    "%Y-%m-%dT%H:%M:%S.%f")

  return datetime.utcnow() - start