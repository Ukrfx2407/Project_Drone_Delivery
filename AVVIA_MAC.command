#!/bin/bash
cd "$(dirname "$0")"
clear
echo "==================================================="
echo "    Preparazione dell'ambiente di simulazione..."
echo "==================================================="
echo ""
echo "Installazione delle librerie necessarie..."
pip3 install customtkinter pillow
echo ""
echo "Avvio dell'interfaccia grafica in corso..."
python3 Drone_GUI.py