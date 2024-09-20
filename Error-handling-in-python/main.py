# try: # Try block is the main execution that will be tried to execute
#     file = open("a_file.txt")
#     a_dict= {"Key": "Value"}
#     print(a_dict["Key"])
# except FileNotFoundError: # if try block Failed then only except block will be executed
#     file= open("a_file.txt", "w")
#     file.write("Something")
# except KeyError as error_message:
#     print(f"The key {error_message} doesn't exist in the above dictionary")
# else: # if try block was sucecssfull then only the else block will be executed
#     content = file.read()
#     print(content)
# finally: # No matter what happened this block will be executed in all of the conditions
#     file.close()

# eval() function will create a list of dictionaries using the input
# facebook_posts = eval(input())
#
# total_likes = 0
# # TODO: Catch the KeyError exception
# for post in facebook_posts:
#   try:
#     total_likes = total_likes + post['Likes']
#   except KeyError:
#     total_likes += 0
#
# print(total_likes)