import os

for root, dirs, files in os.walk('nanome/_internal/'):
    for file in files:
        if file.endswith('.py') and file.startswith('_') and not file.startswith('__init__'):
            # remove the underscore
            old_file = f'{root}/{file}'
            new_file = f'{root}/{file[1:]}'
            os.rename(old_file, new_file)
            # print(cmd)
            # os.system(cmd)
            # print(new_file)

# for root, dirs, files in os.walk('nanome/_internal/'):
#     for dir in dirs:
#         if dir.startswith('_') and not dir.startswith('__pycache__'):
#             old_dir = f'{root}{dir}'
#             new_dir = f'{root}{dir[1:]}'
#             # cmd = f'mv {old_dir}/* {new_dir}'
#             # print(cmd)
#             os.rename(old_dir, new_dir)
#             # print(os.path.join(root, new_dir))
