#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import io
import os
import linecache
import csv

start_interval = 1001
#start_interval = int(raw_input("Введите верхнюю границу целевого интервала: "));
end_interval = 1002
#end_interval = int(raw_input("Введите нижнюю границу целевого интервала: "));
if start_interval>end_interval:
	print("перепутаны верхняя и нижняя границы")
	
count_str = (end_interval - start_interval)*5
GK_data=[]
list_inclinometries_read = []

path_to_supporting_wells = "/home/artem/diplom/КУСТ_142_4863_ГС_ЮК3/3_СОПРОВОЖДЕНИЕ/3.1_ОПОРНЫЕ_СКВАЖИНЫ/"
directories = os.listdir(path_to_supporting_wells)
print(len(directories))
k=0;
nubmer_ASCII=30;
for i in directories:
	path_to_i_supporting_well = path_to_supporting_wells + '' + directories[k]
	files_new = os.listdir(path_to_i_supporting_well)
	for i in files_new:
		#strtest = "Инклинометрия по скв." +directories[k]+ ".csv"
		#print(strtest)
		if i.endswith("Инклинометрия по скв. " +directories[k]+ ".csv"):
			print(i)

			with open(path_to_supporting_wells + directories[k] + '/' + i, "r") as file:
				reader = csv.reader(file)

				line1 = reader.next()
				line2 = reader.next()
				if len(line2)<3:
					print(line2)
					linetest = line2[0]
					s = linetest.split(';')
					inclinometria = int(float(s[4])-float(s[5]))
				else:
					inclinometria = int(float(line2[4])-float(line2[5]))
				print(inclinometria)
				list_inclinometries_read.append(inclinometria)

	k+=1
print(list_inclinometries_read)

list_inclinometries = [i * 5 for i in list_inclinometries_read]
