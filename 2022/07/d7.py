with open('input.txt', 'r') as f:
    contents = f.read()

example_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

# contents = example_input

class Dir:
    def __init__(self, name, parent_dir):
        self.name = name
        self.parent_dir = parent_dir
        self.child_dirs = {}
        # key name value size
        self.files = {}

    def size(self):
        size = sum(self.files.values()) + sum([d.size() for d in self.child_dirs.values()])
        return size


lines = contents.splitlines()
# assume first statement is '$ cd /'
# key name value Dir
current_dir = Dir('/', None)
root_dir = current_dir
dirs = {current_dir.name: current_dir}

ls_mode = False
for line in lines[1:]:
    if line == '$ cd ..':
        current_dir = current_dir.parent_dir
        continue

    if line.startswith('$ cd '):
        child_dir_name = line[5:]
        current_dir = [d for d in current_dir.child_dirs.values() if d.name.endswith(child_dir_name + '/')][0]
        continue

    # Assuming implicitly that we're processing ls results if none of these conditions are met below
    if line == '$ ls':
        continue

    size_or_dir, obj_name = line.split(' ')
    if size_or_dir == 'dir':
        dir_name = current_dir.name + obj_name + '/'
        child_dir = Dir(dir_name, current_dir)
        current_dir.child_dirs[dir_name] = child_dir
        if dir_name in dirs:
            raise ValueError("saatana")
        dirs[dir_name] = child_dir
    else:
        current_dir.files[obj_name] = int(size_or_dir)


at_most_100000_sizes = [dir.size() for dir in dirs.values() if dir.size() <= 100000]
print(sum(at_most_100000_sizes))

# part 2

total_disk_space = 70000000
current_available_space = total_disk_space - root_dir.size()
required_space = 30000000 - current_available_space
print(min([dir.size() for dir in dirs.values() if dir.size() >= required_space]))
