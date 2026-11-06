"""
เขียบนโปรแกรมหา index ของตัวเลขที่มีค่ามากที่สุดใน list

[Input]
numbers: list of numbers

[Output]
index: index of maximum number in list

[Example 1]
input = [1,2,1,3,5,6,4]
output = 5

[Example 2]
input = []
output = list can not blank
"""



class Solution:

    def find_max_index(self, numbers: list) -> int | str:

        # ตรวจสอบว่า List ว่างหรือไม่
        if len(numbers) == 0:
            return "list can not blank"

        # กำหนดค่าเริ่มต้นให้เป็นตัวแรกใน List
        max_number = numbers[0]
        max_index = 0

        # วนลูปตรวจสอบตัวเลขใน List
        for index in range(len(numbers)):

            if numbers[index] > max_number:
                max_number = numbers[index]
                max_index = index

        return max_index


# ส่วนสำหรับ Run โปรแกรม
if __name__ == "__main__":
    solution = Solution()

    # Example 1
    print(solution.find_max_index([1, 2, 1, 3, 5, 6, 4]))
    # Output: 5

    # Example 2
    print(solution.find_max_index([]))
    # Output: list can not blank
