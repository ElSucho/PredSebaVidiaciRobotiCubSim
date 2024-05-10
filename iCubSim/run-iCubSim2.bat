set PATH=C:\Windows\System32
cd bin
start iCub_SIM.exe --name icubSim2
timeout /t 8
set QT_QPA_PLATFORM_PLUGIN_PATH=.
start yarpmotorgui.exe --name icubSim2 --from robotMotorGui.ini
timeout /t 2
cd ..

