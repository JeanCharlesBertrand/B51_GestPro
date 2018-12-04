cd /d %~dp0
call git.exe config --global user.name "shadarnook"
call git.exe config --global user.email "vincentrudel@hotmail.com"
call git.exe config --global user.password "Yolo54321" 
call git.exe add *
call git.exe commit -m "test de push a partir d'un fichier .bat"
call git.exe push origin master --repo https://shadarnook:Yolo54321@domain.name/name/repo.git