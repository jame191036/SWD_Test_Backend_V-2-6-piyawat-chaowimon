"""
เขียบนโปรแกรมแปลงตัวเลยเป็นตัวเลข roman

[Input]
number: list of numbers

[Output]
roman_text: roman number

[Example 1]
input = 101
output = CI

[Example 2]
input = -1
output = number can not less than 0
"""



class Solution:

    def number_to_roman(self, number: int) -> str:

        # ตรวจสอบตัวเลขติดลบ
        if number < 0:
            return "number can not less than 0"

        # กรณีเลขศูนย์
        if number == 0:
            return ""

        # กำหนดค่าตัวเลขและเลขโรมัน เรียงจากมากไปน้อย
        roman_values = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I")
        ]

        roman_text = ""

        # วนลูปแปลงตัวเลขเป็นเลขโรมัน
        for value, roman in roman_values:

            while number >= value:
                roman_text += roman
                number -= value

        return roman_text


# ส่วนสำหรับ Run โปรแกรม
if __name__ == "__main__":
    number = int(input("Enter number: "))

    solution = Solution()
    result = solution.number_to_roman(number)

    print(result)