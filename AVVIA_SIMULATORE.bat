@echo off
title Avvio Simulazione PDDL - Drone
echo ===================================================
echo     Preparazione dell'ambiente di simulazione...
echo ===================================================
echo.
echo Installazione delle librerie necessarie (CustomTkinter, PIL)...
pip install customtkinter pillow >nul 2>&1
echo.
echo Avvio dell'interfaccia grafica in corso...
cd Code
python Drone_GUI.py
pause