# from datetime import datetime
# from time import sleep
# import random
# class Time:
#     id = None
#     time = None

#     def __str__(self) -> str:
#         return f"< Time {self.id} >"
    
# datas = [None for _ in range(1, 11)]
# indexs = []
# index_length = 0
# while index_length != 10:
#     random_index = random.randint(0, 9)
#     if random_index not in indexs:
#         indexs.append(random_index)
#     index_length = len(indexs)
# index = 0
# for _ in range(1, 11):
#     time = Time()
#     random_index = random.randint(0, 8)
#     time.id = _
#     time.time = datetime.now()
#     datas[indexs[index]] = time
#     index += 1
#     sleep(0.05)


# # Example usage
# arr = [5, 3, 7, 2, 8, 1, 4, 6]
# sorted_arr = tree_sort(datas)
# for arr in sorted_arr:
#     print(arr)

