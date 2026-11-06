"""
เขียบนโปรแกรมหาจำนวนเลข 0 ที่ออยู่ติดกันหลังสุดของค่า factorial โดยห้ามใช้ function from math

[Input]
number: as an integer

[Output]
count: count of tailing zero as an integer

[Example 1]
input = 7
output = 1

[Example 2]
input = -10
output = number can not be negative
"""



class Solution:

    def find_tailing_zeroes(self, number: int) -> int | str:
        # ตรวจสอบกรณีเลขติดลบ
        if number < 0:
            return "number can not be negative"

        count = 0

        # นับจำนวนตัวประกอบของ 5
        while number >= 5:
            count += number // 5
            number //= 5

        return count


# ส่วนสำหรับ Run โปรแกรม
if __name__ == "__main__":
    number = int(input("Enter number: "))

    solution = Solution()
    result = solution.find_tailing_zeroes(number)

    print(result)
