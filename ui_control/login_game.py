from anasis import excel_analysis as ea


def login_count():
    return

yys_count = ea.read_excel()
while len(yys_count) > 0:
    find_count = yys_count.pop(0)
    name = find_count.get("账号")



