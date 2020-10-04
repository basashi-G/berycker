from berycker import tools
import re
import paramiko
from termcolor import colored


comment = re.compile(r"# ")
embead = re.compile(r"{.+}")


def read_pickerfile():
    with open("beryckerfile") as f:
        raw_lines = f.readlines()

    formatted_lines = []
    for line in raw_lines:
        stripped_line = line.strip()
        if stripped_line == "":
            pass
        elif comment.match(line) is not None:
            pass
        else:
            formatted_lines.append(stripped_line)
    return formatted_lines


def main():
    hostname = tools.dialog("ホスト名を入力してください", "raspberrypi.local")
    username = tools.dialog("ユーザー名を入力してください", "pi")
    password = tools.dialog("パスワードを入力してください", "raspberry", is_pass=True)

    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)

        step = 1
        commands = read_pickerfile()
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            print(f"Step {step}/{len(commands)} {command}")
            for line in stdout:
                print(f"---> {line}")
            for line in stderr:
                print(colored(f"E: {line}", "red"))
            step += 1


def serch_embead(cmds):
    embead_set = set()
    for cmd in cmds:
        for i in embead.findall(cmd):
            embead_set.add(i)
    return embead_set


def fill_cmd(cmds, embead_set):
    if len(embead_set) == 0:
        return cmds
    else:
        variable = embead_set.pop()
        value = tools.dialog(f"{variable} の値を入力してください")
        return fill_cmd(
            list(map(lambda x: x.replace(variable, value), cmds)),
            embead_set,
        )


if __name__ == "__main__":
    # main()
    text = read_pickerfile()
    print(fill_cmd(text, serch_embead(text)))
