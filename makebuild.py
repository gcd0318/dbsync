import getopt
import os
import sys
import tarfile

PKG = 'pkg.tar.xz'

#一次性打包整个根目录。空子目录会被打包。
def make_tarxz(source_dir, output_filename):
    with tarfile.open(output_filename, "w:xz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

#逐个添加文件打包，未打包空子目录。可过滤文件。
def make_targz_one_by_one(output_filename, source_dir): 
    tar = tarfile.open(output_filename,"w:gz")
    for root,dir,files in os.walk(source_dir):
        for file in files:
            pathfile = os.path.join(root, file)
            tar.add(pathfile)
    tar.close()

if ('__main__' == __name__):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:t:", ["help", "src=", "tgt="])
    except getopt.GetoptError:
        print('-s <src> -t <tgt>')
        print('or')
        print('--src=<src> --tgt=<tgt>')
        sys.exit(2)

    src, tgt = None, None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('-s <src> -t <tgt>')
            print('or')
            print('--src=<src> --tgt=<tgt>')
        elif opt in ("-s", "--src"):
            src = arg
        elif opt in ("-t", "--tgt"):
            tgt = arg

    if (src and tgt) is not None:
        if not tgt.endswith(PKG):
            tgt = tgt + os.sep + PKG
        make_tarxz(src, tgt)
