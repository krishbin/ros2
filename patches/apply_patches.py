import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(root_dir, 'src')
patches_dir = os.path.join(root_dir, 'patches')

def listpatches_location(out,path):
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            listpatches_location(out,os.path.join(path, f))
        else:
            out.add(os.path.join(path, f))

def get_src_path(patch_path):
    a = patch_path.split('/')
    a.pop(-1)
    path = '/'.join(a)
    return path.replace(patches_dir, src_dir)

if __name__ == '__main__':
    patches = set()
    listpatches_location(patches,patches_dir)
    patches.remove(os.path.join(patches_dir, 'apply_patches.py'))
    for patch in patches:
        src_path = get_src_path(patch)
        if os.path.exists(src_path):
            print(f'\npatch: {patch}')
            print('patching: %s' % src_path)
            if os.system(f'cd {src_path} && git reset --hard && git apply {patch}') != 0:
                print('failed to apply patch %s' % patch)
                exit(1)
            print('applied patch\n')
        else:
            print('skipping: %s' % src_path)