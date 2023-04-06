import pkgutil

# Đường dẫn tới thư mục chứa các module
path = ["./"]

# Duyệt và in ra tất cả các module trong thư mục
for module in pkgutil.walk_packages(path):
    if module.name.split(".")[0] != "airflow":
        print(module.name)
