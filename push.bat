cd /d %~dp0
call git.exe config --global user.name "shadarnook"
call git.exe config --global user.email "vincentrudel@hotmail.com"
call git.exe config remote.origin.url https://shadarnook:Yolo54321@github.com/JeanCharlesBertrand/B51_GestPro
call git.exe add *
call git.exe commit -m "nouveau test"
call git.exe push
pause