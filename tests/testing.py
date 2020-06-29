#!/usr/bin/env python3
import sys, os
import json, csv
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QVBoxLayout, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt, QUrl
import traceback
import requests
import rightside

window = rightside.Ledger()
window.addItem()
