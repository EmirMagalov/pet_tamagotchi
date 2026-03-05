from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "pets" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "telegram_id" BIGINT NOT NULL UNIQUE,
    "name" VARCHAR(50),
    "money" REAL NOT NULL DEFAULT 100,
    "hunger" REAL NOT NULL DEFAULT 100,
    "energy" REAL NOT NULL DEFAULT 100,
    "dirt" REAL NOT NULL DEFAULT 0,
    "last_updated" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_sleeping" INT NOT NULL DEFAULT 0,
    "wake_up_at" BIGINT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztl1Fv2jAQx78K4olKXUUDFLY3QunKBKSidJtaVZFJjmDh2FnirEVVv/tskxCSAAtdu7"
    "ZSnyD/u4t9P9vx3UPZZTaQ4OgCePlL6aFMkQviz7p8WCojz0tEKXA0IcrPA64ENAm4jyz5"
    "kikiAQjJhsDysccxo0KlISFSZJZwxNRJpJDiXyGYnDnAZ+ALw82tkDG14R6C+NGbm1MMxE"
    "7NEttybKWbfOEprUf5mXKUo01Mi5HQpYmzt+AzRlfemKoEHaDgIw7y9dwP5fTl7KIs44yW"
    "M01cllNci7FhikLC19ItyMBiVPITswlUgo4c5ZN2XG/WW7WTeku4qJmslObjMr0k92WgIj"
    "Aclx+VHXG09FAYE24cCDg+cs1NAHXsbGWYCfw7zBjdG6D5WdNqtaZWrZ20GvVms9GqrrDm"
    "Tbv46r2vErFwYGLLL89BzDxhrH5zcDsz5G9GG/tnmIpECjCNiK2Qxi4J0+RUPhNUF92bBK"
    "jDZ+KxUd3B63t71DlvjyqN6kEa2jCyaMqUxucyCos8vzPC0Ja9uYrIEJzKkKfsyyIQj6vV"
    "o+rTKe6gdmpc6f1u6WLU7fQue8ZQZuAugl8kMUpJCJirPEfddj8DcRZSB/y9KCYhHxhjjD"
    "JhZ7/NmIR8YIwx2tjne0GMA/4nwrcMkKCAm6Fnq5RzIE+FzLELm1lmYzNM7Sj4KP7zUnz/"
    "8dbxAdkGJYvoztsBfNwbdC/H7cGFIh3EpNvjrrRoaf6RWjnJ3FCrl5R+9MbnJflYujaGaq"
    "k8FnDHVyMmfuPrspwTCjkzKbszkb1W0MRqDCa1uDgwAwLgyfTzNRljBBDdUtimIzMrOxGh"
    "L7WY+5b6xY+Lbhj91MLpvUzFNbwa6N1R5fggfWzyhdgdmoPY+Sba8PHZVeum456n1C30BX"
    "oPla5syabzteZCChNkze+Qb5s5C9PYNt+8ydXcrIIochQumbeccNSftsHH1qy8oXONLIe7"
    "mleU+Hy0r8/5lX7h9vU3+IGcUg7e9u5qLeRJDdZr3HWpDktrNAq0WMJra4+lbOlPozwae0"
    "CM3N8nQFEbFwAovLYCVLY0QDEiB7rhYvl2aQw3Q1wLyYC8oiLBGxtb/LBEcMBv3ybWHRRl"
    "1qlbO4ZXGbR/Zrl2+oaeraPkC/TXvl4e/wAtd6yG"
)
