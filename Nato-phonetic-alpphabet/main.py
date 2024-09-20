import pandas
# student_dict={
#     "student":["Angela", "James", "Lilly"],
#     "score":[56, 76, 98]
# }
# new_student_dataFrame=pandas.DataFrame(student_dict)
# for (index, row) in new_student_dataFrame.iterrows():
#     if row.student=="Angela":
#         print(row.score)


df =pandas.read_csv("nato_phonetic_alphabet.csv")
new_dict={row.letter:row.code for (index,row) in df.iterrows()}
input_word=list(input("Enter a word: ").upper())
phonetic_alphabetic_list=[new_dict[item] for item in input_word]
print(phonetic_alphabetic_list)