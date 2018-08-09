#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import io
import os
import linecache
import csv


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
#print(len(directories))
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

print ("GK_data",GK_data)


print ("GK_data element",GK_data[2])

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