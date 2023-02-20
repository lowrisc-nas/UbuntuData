import subprocess

import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import email_helper as mail


def main():

  # Initialize the email
  msg = MIMEMultipart()

  msg['Subject'] = "NAS Status: " + datetime.datetime.now().strftime("%Y-%m-%d")
  msg['From'] = mail.USERNAME
  msg['To'] = mail.USERNAME

  # Pool Status
  summary = f"<h2>POOL Status</h2>\n"

  zpool_status = subprocess.check_output(['zpool', 'list', '-v']).decode('utf-8').split("\n")
  zpool_status = [[val for val in line.split()] for line in zpool_status]

  summary += mail.wrap_html(mail.table2html(zpool_status))

  # Pool Usage
  summary += f"<h2>POOL Usage</h2>\n"
  pool_status = subprocess.check_output(['zfs', 'list']).decode('utf-8').split("\n")
  pool_status = [[val for val in line.split()] for line in pool_status]

  summary += mail.wrap_html(mail.table2html(pool_status))

  # Docker Status
  summary += f"<h2>Docker Status</h2>\n"
  dformat = "{{.Names}}\t{{.Image}}\t{{.State}}\t{{.Status}}\t{{.RunningFor}}"
  docker_status = subprocess.check_output(['docker', 'ps', '--format', dformat]).decode('utf-8').split("\n")
  docker_tbl  = [['Name', 'Image', 'State', 'Status', 'Running For']]
  docker_tbl += [[val for val in line.split('\t')] for line in docker_status]

  summary += mail.wrap_html(mail.table2html(docker_tbl))

  # Header for details section
  summary += "<h2>Details</h2>"

  # Detailed Pool Status
  body = "\n================ Detailed POOL STATUS ================\n"
  zpool_status = subprocess.check_output(['zpool', 'status']).decode('utf-8').split("\n")

  for line in zpool_status:
    body += f"{line.strip()}\n"

  # Construct and send the email
  msg.attach(MIMEText(summary, "html"))
  msg.attach(MIMEText(body, "plain"))

  mail.send_email(msg)


if __name__ == '__main__':
  main()