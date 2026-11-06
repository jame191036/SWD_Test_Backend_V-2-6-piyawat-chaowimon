"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_thai(self, number: int) -> str:

        # ตรวจสอบตัวเลขติดลบ
        if number < 0:
            return "number can not less than 0"

        # กรณีเลขศูนย์
        if number == 0:
            return "ศูนย์"

        # คำอ่านตัวเลข
        thai_numbers = [
            "ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่",
            "ห้า", "หก", "เจ็ด", "แปด", "เก้า"
        ]

        # คำอ่านตามหลักตัวเลข
        thai_positions = [
            "", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน"
        ]

        def convert_under_million(num):

            if num == 0:
                return ""

            result = ""
            digits = str(num)
            length = len(digits)

            for index, digit in enumerate(digits):

                digit = int(digit)
                position = length - index - 1

                if digit == 0:
                    continue

                # หลักสิบ
                if position == 1:
                    if digit == 1:
                        result += "สิบ"
                    elif digit == 2:
                        result += "ยี่สิบ"
                    else:
                        result += thai_numbers[digit] + "สิบ"

                # หลักหน่วย
                elif position == 0:
                    if digit == 1 and length > 1:
                        result += "เอ็ด"
                    else:
                        result += thai_numbers[digit]

                # หลักร้อยขึ้นไป
                else:
                    result += thai_numbers[digit] + thai_positions[position]

            return result

        # กรณีตัวเลขตั้งแต่หนึ่งล้านขึ้นไป
        if number >= 1_000_000:
            million = number // 1_000_000
            remainder = number % 1_000_000

            result = convert_under_million(million) + "ล้าน"

            # เศษเป็น 1 และมีหลักล้านนำหน้า จึงต้องอ่านว่า "เอ็ด" ไม่ใช่ "หนึ่ง"
            if remainder == 1:
                result += "เอ็ด"
            else:
                result += convert_under_million(remainder)

            return result

        return convert_under_million(number)

# ส่วนสำหรับ Run โปรแกรม
if __name__ == "__main__":
    number = int(input("Enter number: "))

    solution = Solution()
    result = solution.number_to_thai(number)

    print(result)