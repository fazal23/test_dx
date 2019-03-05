import os
import sys
import json
import shlex
import subprocess
import commands
from github import Github
from requests import get


def check_perms(username, policyName, github_access_token):
    print "inside check_permissions for non admin user"
    g = Github(base_url="REPO LINK", login_or_token=github_access_token)
    repo = g.get_repo("REPONAME")
    print(policyName)
    contents = repo.get_contents("policies/{}".format(policyName), ref="Branch NAME")
    link = contents.raw_data['download_url']
    header_token= 'token ' + github_access_token
    headers = {'Authorization': header_token}
    r = get(link, headers)
    file_content = r.text
    print('Policy Contains')
    print(file_content)
    if  "write" in file_content:
        content = '''path \"secret/{0}" {{
                policy = "read"
            }}

            path "secret/{0}/*" {{
                policy = "read"
            }}'''.format(username)
        os.system("echo -e '{}' > {}.hcl".format(content,username))
        print(commands.getoutput('ls'))
        print(commands.getoutput('cat {}.hcl'.format(username)))
        commands.getoutput('chmod +x vault.sh')
        commands.getoutput('/bin/bash vault.sh')
    else:
        print('User operations allowed')
        os.system('./vault.sh')

def main():

    github_access_token = sys.argv[1]
    vault_login_token = sys.argv[2]

    g = Github(base_url="REPO LINK", login_or_token=github_access_token)

    org = g.get_organization('cloudops')

    cmd = "curl -H \"Authorization: token "+github_access_token+"\" -X GET  MASTER COMMMITS LINK OF REPO "
    cmd3 = 'ls -1t policies/ | head -1'
    args1 = shlex.split(cmd3)
    #print("Args::", args1)
    process = subprocess.Popen(args1, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output1, err = process.communicate()
    print "list of files"
    print output1
    policyName = output1.split("\n")[1]
    policy_commiter_name = policyName.strip(".hcl")
    print policyName
    print policy_commiter_name 
    os.environ["POLICYNAME"] = policyName
    os.environ["POLICYCOMMITERNAME"] = policy_commiter_name

    
    
    args = shlex.split(cmd)
    print("Args::", args)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    # print output

    # print type(output)

    op = json.loads(output)

    commit_url = op["object"]["url"]
    # print(commit_url)

    cmd2 = "curl -H \"Authorization: token "+github_access_token+"\" -X GET "+ commit_url

    args = shlex.split(cmd2)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()

    # print output

    # print type(output)

    op = json.loads(output)

    print op

    last_commiter_name = op["author"]["name"]

    print (last_commiter_name)
    print("last_commiter_name: {} policy_commiter_name: {} policyName: {}".format(last_commiter_name,policy_commiter_name,policyName))


    teams = org.get_teams()

    vault_admin = 'Vault_Admins'
    vault_users = 'Vault_Users'
    filtered_teams = []

    for t in teams:
        if vault_admin in t.name or vault_users in t.name:
            filtered_teams.append(t)

    users_dict = {}

    for t in filtered_teams:
        temp_members = t.get_members()
        names = []
        for m in temp_members:
            names.append(m.name)
        users_dict[t.name] = names

    print(users_dict)

    is_vault_admin_user = False
    is_vault_nonadmin_user = False

    if last_commiter_name in users_dict['Vault_Users']:
        is_vault_nonadmin_user = True
    elif last_commiter_name in users_dict['Vault_Admins']:
        is_vault_admin_user = True
    else:
        pass

    # sciptname = "first.sh"
    if is_vault_admin_user:
        # set the env vari = $RTOKEN | $POLICYNAME | $WORKSPACE
        commands.getoutput('chmod +x vault.sh')
        commands.getoutput('/bin/bash vault.sh')
        # pass
    else:
        check_perms(policy_commiter_name , policyName, github_access_token)

if __name__ == "__main__":
    main()
