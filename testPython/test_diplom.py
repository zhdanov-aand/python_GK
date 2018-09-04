#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import io
import os
import linecache
import csv
import numpy as np
import random

start_interval = 100
#start_interval = int(raw_input("Введите верхнюю границу целевого интервала: "));
end_interval = 110
#end_interval = int(raw_input("Введите нижнюю границу целевого интервала: "));
if start_interval>end_interval:
	print("перепутаны верхняя и нижняя границы")
	
count_str = (end_interval - start_interval)*5
GK_data=[]

path_to_supporting_wells = "/home/artem/diplom/КУСТ_142_4863_ГС_ЮК3/3_СОПРОВОЖДЕНИЕ/3.1_ОПОРНЫЕ_СКВАЖИНЫ/"
directories = os.listdir(path_to_supporting_wells)
# print(len(directories))
k=0;
nubmer_ASCII=30;
list_inclinometries_read = []

for i in directories:
	path_to_i_supporting_well = path_to_supporting_wells + '' + directories[k]
	files_new = os.listdir(path_to_i_supporting_well)
	for i in files_new:
		#strtest = "Инклинометрия по скв." +directories[k]+ ".csv"
		#print(strtest)
		if i.endswith("Инклинометрия по скв. " +directories[k]+ ".csv"):
			#print(i)

			with open(path_to_supporting_wells + directories[k] + '/' + i, "r") as file:
				reader = csv.reader(file)

				line1 = reader.next()
				line2 = reader.next()
				if len(line2)<3:
					#print(line2)
					linetest = line2[0]
					s = linetest.split(';')
					inclinometria = int(float(s[4])-float(s[5]))
				else:
					inclinometria = int(float(line2[4])-float(line2[5]))
				#print(inclinometria)
				list_inclinometries_read.append(inclinometria)

	k+=1
print('Инклинометрия из exsel файлов: ',list_inclinometries_read)

list_inclinometries = [i * 5 for i in list_inclinometries_read]
k=0
for i in directories:
	print ('Скважина:',i)
	GK_data.append([])
	path_to_i_supporting_well = path_to_supporting_wells + '' + directories[k]
	files_new = os.listdir(path_to_i_supporting_well)
	for i in files_new:
		if i.endswith(".MKRH.las"):
			print ('Файл с GK:',i)
			word_for_search = str(start_interval) + '.00'
			#print (path_to_supporting_wells + directories[0] + i +'')

			with io.open(path_to_supporting_wells + directories[k] + '/' + i, encoding='ISO-8859-1') as file:
				count_for_search_line=0
				for line in file:
					if word_for_search in line:
						#print(line, end='')
						print('Номер строки, откуда начнём считывать .las файл (без учета инклинометрии):',count_for_search_line)
						break
					count_for_search_line+=1

			f_1 = open(path_to_supporting_wells + directories[k] + '/' + i, 'r')
			#with io.open(path_to_supporting_wells + directories[k] + '/' + i, encoding='ISO-8859-1') as file:		
			for j in range(count_str):
				#l=f_1.read(j+2)

				#print('символы' + l)
				#print('номер строки с которой начнём')
				number = count_for_search_line+j+list_inclinometries[k]
				#print(number)
				#line = linecache.getline(path_to_supporting_wells + directories[k] + '/' + i, nubmer_ASCII+j+list_inclinometries[k])
				line = linecache.getline(path_to_supporting_wells + directories[k] + '/' + i, count_for_search_line+j+list_inclinometries[k])
				print ('Строка',number,":",line)
				if line == "":
					break
				#print('работа со строкой')
				s = line.split('\t')
				#print('Новая строка')
				#print(s)
				#print ('Длина')
				#print(len(s))

				s0 = s[0]
				s1 = s0.split(' ')
				#print(float(s1[1]))

				s00 = s[1]
				s11 = s00.split('\t')
				print('Отформатированное значение GK: ',float(s11[0]))
				GK_data[k].append(float(s11[0]))
			f_1.close()

	k+=1


print ("inclinometries with koeff 5", list_inclinometries)

#print ("GK_data",GK_data)


for i in range(len(GK_data)):
	for j in range(len(GK_data[i])):
		if GK_data[i][j] == -999.25:
			GK_data[i][j]=0;



#print ("GK_data element",GK_data[2])

#a=np.random.uniform(1, 10, (1, len(GK_data[0])))
GK_new_well = np.random.uniform(1, 8,  len(GK_data[0]))
print ("GK_data",GK_data,"test")
print ("GK_new_well",GK_new_well)


GK_min_raznost=[]
for i in range(len(GK_new_well)):
	# GK_min_raznost[i]=abs(GK_new_well[i]-GK_data[0][i])
	GK_min_raznost.append(abs(GK_new_well[i]-GK_data[0][i]))
	for j in range(len(GK_data)-1):
		if abs(GK_new_well[i]-GK_data[j+1][i])<GK_min_raznost[i]:
			# GK_min_raznost[i]=abs(GK_new_well[i]-GK_data[j+1][i])
			del GK_min_raznost[len(GK_min_raznost)-1]
			GK_min_raznost.append(abs(GK_new_well[i]-GK_data[j+1][i]))

print("GK_min_raznost",GK_min_raznost)


# print("MODYL",abs(GK_new_well[2]-GK_data[0][2]),"Что лежит в массиве",GK_min_raznost[2])


GK_number_well_with_min_raznost=[]
for i in range(len(GK_new_well)):
	GK_number_well_with_min_raznost.append(0)
	for j in range(len(GK_data)-1):
		if abs(GK_new_well[i]-GK_data[j+1][i]) == GK_min_raznost[i]:
			# print("MODYL",abs(GK_new_well[i]-GK_data[j+1][i]),"Что лежит в массиве",GK_min_raznost[i])
			del GK_number_well_with_min_raznost[len(GK_number_well_with_min_raznost)-1]
			GK_number_well_with_min_raznost.append(j+1)

print("GK_number_well_with_min_raznost",GK_number_well_with_min_raznost)


GK_good_with_all_wells=[]
for i in range(len(GK_number_well_with_min_raznost)):
	for k in range(len(directories)):
		if GK_number_well_with_min_raznost[i] == k:
			GK_good_with_all_wells.append(GK_data[k][i]);

print("GK_good_with_all_wells",GK_good_with_all_wells)



GK_name_well_with_min_raznost=list(GK_number_well_with_min_raznost)
# print("GK_name_well_with_min_raznost",GK_name_well_with_min_raznost,len(GK_name_well_with_min_raznost))


# print(directories)


for i in range(len(GK_name_well_with_min_raznost)):
	for k in range(len(directories)):
		if GK_name_well_with_min_raznost[i] == k:
			GK_name_well_with_min_raznost[i]=directories[k];

print("GK_name_well_with_min_raznost",GK_name_well_with_min_raznost)




nearest_well = None # наиболее часто встречаемое значение
count_nearest_well = 0
for item in GK_name_well_with_min_raznost:
    # переменной count присваивается количество случаев
    # item в списке a
    count = GK_name_well_with_min_raznost.count(item)
    # Если это количество больше максимального,
    if count > count_nearest_well:
        count_nearest_well = count # то заменяем на него максимальное,
        nearest_well = item # запоминаем само значение

# вывод значения на экран
print("Ближайшая скважина: ",nearest_well)




#print (a,len(a),len(GK_data[1]))
# word = u'100.00'
# k=0
# with io.open('/home/artem/diplom/КУСТ_142_4863_ГС_ЮК3/3_СОПРОВОЖДЕНИЕ/3.1_ОПОРНЫЕ_СКВАЖИНЫ/540г/540Р_GK.MKRH.las', encoding='ISO-8859-1') as file:
#     for line in file:
#         if word in line:
#             print(line, end='')
#             print(k)
#         k+=1
# reg_name='_GK'

# f_1 = open(path_to_i_supporting_well + 'test.txt')
# l = f_1.read(1)
# print l

# from os import listdir
# from os.path import isfile, join

# path1 = '/home/artem/diplom/КУСТ_142_4863_ГС_ЮК3'

# onlyfiles = [f for f in listdir(path1) if isfile(join('/home/artem/work/diplom/КУСТ_142_4863_ГС_ЮК3', f))]
# print onlyfiles

#files = os.listdir("../testPython")
#print files
# import pandas as pd
# import os


# def get_data(path, well_number = 1, sep=',', header=None):
#     abs_path = os.path.abspath('../') # абсолютный путь до папки, где находишься. '../' - на уровень вверх от текущего уровня
#     path = os.path.join(abs_path, 'well_log_data', path, path + '.' + str(well_number) + '.csv') # формирование обещго пути до файла
# 	return pd.read_csv(path, sep=sep, header=header)