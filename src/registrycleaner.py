import requests
import argparse
import os.path
import json
import base64

parser = argparse.ArgumentParser(description='Example usage: python {} --host registry-url --username '
                                             'registry-username --password registry-password --get-tags '
                                             'repo-name'.format(os.path.basename(__file__)),
                                 epilog='Must be installed : "pip install requests" and "pip install argparse"')

parser.add_argument('--host','-host', metavar='registry-url', nargs='+',
                    help='Registry URL')

parser.add_argument('--username','-u', metavar='registry-user', nargs='+',
                    help='Registry user')

parser.add_argument('--password','-p', metavar='registry-password', nargs='+',
                    help='Registry user password')

parser.add_argument('--get-repos', help='Add this parameter to see all repos',
                    action='store_true')

parser.add_argument('--get-tags', metavar='repo-name', nargs='+',
                    help='Add this parameter to see all tags of written repo')

parser.add_argument('--yes', help='Add this parameter to delete tags',
                    action='store_true')

parser.add_argument('--tag','-t', metavar='taglist', nargs='+',
                    help='Write repo and tags you want to delete, like "repo1:tag1 repo1:tag2 repo2:tag repo3:*".'
                         ' Write "*" instead of tag to delete all tags of repository')

parser.add_argument('--already-login', help='Use if you already login your private docker registry.',
                    action='store_true')

parser.add_argument('--config','-c', metavar='config', nargs='+',
                    help='If you want to specify config path.')

args = parser.parse_args()

def main():
  if (args.get_repos or args.get_tags or args.tag) and (args.already_login or (args.username and args.password)):
    if args.already_login:

      if args.config == None :
        userhome = os.path.expanduser('~')
        with open(userhome + "/.docker/config.json", "r") as f:
          dist = json.load(f)

      else:
        with open("{}".format(args.config[0]), "r") as f:
          dist = json.load(f)

      for k, v in dist[u'auths'].items():
        if k == args.host[0]:
          basic_auth = v[u'auth']

      basic_auth = base64.standard_b64decode(basic_auth).decode("utf-8").split(":")
      uname = basic_auth[0]
      passwd = basic_auth[1]
      auth = uname, passwd
    else:
      auth = '{}'.format(args.username[0]), '{}'.format(args.password[0])

    headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
    url = "https://{}/v2/".format(args.host[0])


    def checkrepo(repo):
      r = requests.get(url + "{}/tags/list".format(repo), headers=headers, auth=auth)
      if r.status_code == 200 and r.json()[u'tags'] is None:
        print("There is no tag in {} repository.".format(repo))
        return 0
      elif r.status_code != 200:
        print("{} : ".format(repo) + r.json()[u'errors'][0][u'message'].title())
        return 0
      else:
        return r.json()[u'tags']


    def checktag(repo, tag):
      if tag == "*":
        r = requests.get(url + "{}/tags/list".format(repo), auth=auth)
        r = r.json()
        for t in r[u'tags']:
          print(repo + " : " + t)
      else:
        r = requests.get(url + "{}/manifests/{}".format(repo, tag), auth=auth)
        if r.status_code == 200:
          print(repo + " : " + tag)
        else:
          print("Tag {} doesn't exist in {} repository.").format(tag, repo)


    def getrepos():
      r = requests.get(url + "_catalog", headers=headers, auth=auth)
      r = r.json()[u'repositories']
      for repo in sorted(r):
        print(repo)


    def gettags(repo):
      if checkrepo(repo) != 0:
        for tag in sorted(checkrepo(repo)):
          print(tag)


    r = requests.get(url, headers=headers, auth=auth)

    # Authentication Control
    if r.status_code == 401:
      print(r.json()[u'errors'][0][u'message'].title())
      exit(1)

    else:
      if args.get_repos:
        getrepos()
      if args.get_tags != None:
        gettags(args.get_tags[0])

      if args.get_repos == False and args.get_tags is None:

        if not args.yes:
          print("Repos to be deleted:\n")

        for x in args.tag:
          b = x.split(":")
          repo = b[0]
          tag = b[1]
          if checkrepo(repo) == 0:
            continue
          else:
            if not args.yes:
              checktag(repo, tag)
            else:
              if tag == "*":
                tagresponse = requests.get(url + "{}/tags/list".format(repo), auth=auth)
                a = tagresponse.json()
                for tags in a[u'tags']:
                  r = requests.get(url + "{}/manifests/{}".format(repo, tags), headers=headers, auth=auth)
                  if r.status_code == 200:
                    response = r.headers['Docker-Content-Digest']
                    r = requests.delete(url + "{}/manifests/{}".format(repo, response), auth=auth)
                    print("{}:{} has been deleted.".format(repo, tags))

              else:
                r = requests.get(url + "{}/manifests/{}".format(repo, tag), headers=headers, auth=auth)
                if r.status_code == 200:
                  response = r.headers['Docker-Content-Digest']
                  print(response)
                  r = requests.delete(url + "{}/manifests/{}".format(repo, response), auth=auth)
                  print("{}:{} has been deleted.".format(repo, tag))
                else:
                  print("Tag {} doesn't exist in {} repository.").format(tag, repo)

  else:
    print ("Please enter required values.")
if __name__ == '__main__':
    main()
