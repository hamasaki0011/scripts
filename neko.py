#/* neko.py */
import os
import sys
import shutil

#outputフォルダを再生成しフォルダパス取得
def getOutputPath():
  os.chdir(os.path.dirname(sys.argv[1]))
  print(f'os.path = {os.path}')
  if(os.path.isdir('output/')):
    shutil.rmtree(os.getcwd()+'output')
  os.mkdir(os.getcwd()+'output')
  os.chdir('output')
  return os.getcwd()

# main function
if __name__ == "__main__":
  print ("-------------- start --------------")
  
  # str = os.path.dirname(sys.argv[0])
  # str = sys.argv[1]
  outfilepath = getOutputPath()
  print(f"outfilepath = {outfilepath}") 
  outfilename = outfilepath + '/NECO.txt'
  # outfilename = 'output' + '/NECO.txt'

  if (os.path.isfile(outfilename)):
    os.remove(outfilename)
  f = open(outfilename, 'x', encoding='UTF-8')
  f.write('2月22日は「ニャン・ニャン・ニャン」で猫の日です\n')
  f.close()

  print ("-------------- end --------------")

