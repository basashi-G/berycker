import psutil
from berycker.tools import dialog, y_or_n, error

template = """country=JP
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="%s"
    psk="%s"
}"""


def main():
    disk_path = dialog("bootドライブのパスを入力してください。", get_boot_path())
    enable_ssh = y_or_n("SSHをオンにしますか？")
    enable_wifi = y_or_n("wifiをオンにしますか？")
    if enable_wifi is True:
        ssid = dialog("SSIDを入力してください", "")
        pawd = dialog("パスワードを入力してください", "", is_pass=True)

    confirm = y_or_n("ファイルを生成しますか？")
    if confirm:
        if enable_wifi:
            filled_template = template % (ssid, pawd)
            generate_file(
                generate_path(disk_path, "wpa_supplicant.conf"), filled_template
            )
        if enable_ssh:
            generate_file(generate_path(disk_path, "ssh"), "")


def generate_file(path, content):
    with open(path, mode="w") as f:
        f.write(content)


def generate_path(drive, filename):
    return f"{drive}:\\{filename}"


def get_boot_path():
    partitions = psutil.disk_partitions()
    for i in partitions:
        if i.fstype == "FAT32":
            return i.mountpoint[0]
    error("適切なフォーマットのSDカードがありません")


if __name__ == "__main__":
    main()
