

folder=$1
lista=$2

mkdir  -p $folder
cd $folder
wget --content-disposition --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --content-disposition -i ../$2 



