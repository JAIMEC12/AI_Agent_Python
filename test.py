from functions.get_files_info import get_files_info, get_file_content

print(get_files_info("calculator","."))
print(get_files_info("calculator", "pkg"))
print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "../"))


print(get_file_content("calculator", "../"))