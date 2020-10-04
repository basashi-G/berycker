from berycker import tools
from berycker.statements import RunCmd, Comment, AddLine, SetIp, SetSSHKey, SetHostName
import re
import paramiko
from termcolor import colored


embead = re.compile(r"{.+}")


def read_pickerfile():
    with open("beryckerfile") as f:
        raw_lines = f.readlines()

    formatted_lines = []
    for line in raw_lines:
        stripped_line = line.strip()
        if stripped_line == "":
            pass
        else:
            formatted_lines.append(stripped_line)
    return formatted_lines


def main():
    hostname = tools.dialog("ホスト名を入力してください", "raspberrypi.local")
    username = tools.dialog("ユーザー名を入力してください", "pi")
    password = tools.dialog("パスワードを入力してください", "raspberry", is_pass=True)

    raw = read_pickerfile()
    filled = fill_cmd(raw, serch_embead(raw))
    interpreted_cmds = convert_to_python_structure(filled, [])

    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)

        step = 1
        for command in interpreted_cmds:
            stdin, stdout, stderr = ssh.exec_command(command)
            print(f"Step {step}/{len(interpreted_cmds)} {command}")
            for line in stdout:
                print(f"---> {line}")
            for line in stderr:
                print(colored(f"E: {line}", "red"))
            step += 1
    print(colored("Complete Successfully!!", "green"))
    print("Thank you for using.")


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


def fitting(statement, line):
    if statement.pattern.fullmatch(line) is not None:
        return statement.apply(*statement.pattern.fullmatch(line).groups())
    else:
        return False


def convert_to_python_structure(input, output):
    if len(input) == 0:
        return output
    else:
        line = input.pop(0)
        if fitting(RunCmd, line):
            fitting_result = fitting(RunCmd, line)
        elif fitting(SetHostName, line):
            fitting_result = fitting(SetHostName, line)
        elif fitting(AddLine, line):
            fitting_result = fitting(AddLine, line)
        elif fitting(SetIp, line):
            fitting_result = fitting(SetIp, line)
        elif fitting(SetSSHKey, line):
            fitting_result = fitting(SetSSHKey, line)
        elif fitting(SetHostName, line):
            fitting_result = fitting(SetHostName, line)
        elif fitting(Comment, line):
            return convert_to_python_structure(input, output)
        else:
            raise SyntaxError("There is a syntax problem with the becyckerfile.")
        return convert_to_python_structure(input, output + fitting_result)


if __name__ == "__main__":
    main()
