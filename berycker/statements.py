import re


class Statement:
    @classmethod
    def apply():
        pass

    @classmethod
    def pattern():
        pass


class AddLine(Statement):
    pattern = re.compile(r'^ADD "(.+)" (\S+)$')

    @classmethod
    def apply(cls, line, path):
        return [f'sudo sh -c "echo {line} >> {path}"']


class SetSSHKey(Statement):
    pattern = re.compile(r"^SSH (.+)$")

    @classmethod
    def apply(cls, key):
        return [
            "mkdir .ssh",
            "touch .ssh/authorized_keys",
            "chmod 700 .ssh",
            "chmod 600 .ssh/authorized_keys",
            f"echo {key} >> .ssh/authorized_keys",
        ]


class RunCmd(Statement):
    pattern = re.compile(r"^RUN (.+)$")

    @classmethod
    def apply(cls, cmd):
        return [cmd]


class SetIp(Statement):
    pattern = re.compile(r"^IP (\S+)$")

    @classmethod
    def apply(cls, ip):
        path = "/etc/dhcpcd.conf"
        router_ip = re.sub(r"(?<=\.)[0-9]+$", "1", ip)
        return list(
            map(
                flat,
                [
                    AddLine.apply("interface eth0", path),
                    AddLine.apply(f"static ip_address={ip}/24", path),
                    AddLine.apply(f"static routers={router_ip}", path),
                    AddLine.apply(f"static domain_name_servers={router_ip}", path),
                ],
            )
        )


class Comment(Statement):
    pattern = re.compile(r"^# .+$")

    @classmethod
    def apply(cls):
        # applyの結果を真偽値に変換してマッチするかどうかも兼ねているため、Trueを返してマッチすることを伝える
        return True


# ラズパイのみ対応
class SetHostName(Statement):
    pattern = re.compile(r"^HOSTNAME (\S+)$")

    @classmethod
    def apply(cls, hostname):
        return [f"sudo raspi-config nonint do_hostname {hostname}"]


def flat(solo_list):
    return solo_list[0]


if __name__ == "__main__":
    if "ca":
        print("hge")
