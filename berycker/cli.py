import fire
from berycker import build
from berycker import initialize


def main():
    fire.Fire(
        {
            "init": initialize.main,
            "build": build.main,
        }
    )


if __name__ == "__main__":
    main()
