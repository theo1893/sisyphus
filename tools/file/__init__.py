from tools.file.local_fs import LocalFS

local_fs = None


def initialize():
    global local_fs
    local_fs = LocalFS()
