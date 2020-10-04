from getpass import getpass


def dialog(prompt, default="", is_pass=False):
    if is_pass:
        input_func = getpass
    else:
        input_func = input
    answer = input_func(f"{prompt} [{default}]: ")
    if answer == "":
        return default
    else:
        return answer


def y_or_n(prompt):
    answer = input(f"{prompt}(y/n) [y]: ")
    if answer == "y":
        return True
    elif answer == "":
        return True
    elif answer == "n":
        return False

    else:
        return error("不正な値が入力されました。変更を取り消します。")


def error(message):
    print(message)
    quit()
