#деление столбиком двух натуральных чисел

# !/usr/bin/env python3

def long_division(dividend, divider):
    ans = str(dividend) + '|' + str(divider)
    strDividend = str(dividend)
    i = 1
    subStr = strDividend[0]

    while i < len(strDividend) and int(strDividend[0:i]) // divider == 0:
        subStr += strDividend[i]
        i += 1

    if strDividend == subStr:
        ans += '\n' + subStr + '|' + str(dividend // divider)
        if int(subStr) >= divider:
            ans += '\n' + ' ' * (len(subStr) - 1) + '0'
        return ans
    else:
        ans += '\n' + str((int(subStr) // divider) * divider)
        ans += ' ' * int(len(strDividend) - len(subStr))
        ans += '|' + str(dividend // divider)

    HelpI = ((int(subStr) // divider) * divider)
    i = len(subStr) - len(str((int(subStr) - HelpI)))
    subStr = str(int(subStr) - HelpI)
    k = i + len(subStr) - 1

    while k < len(strDividend):
        if subStr == '0':

            if strDividend[k + 1] != '0':
                subStr = strDividend[k + 1]
                i += 1
                k += 1

            if i < len(strDividend) - 1 and int(strDividend[i + 1:]) == 0:
                return ans + '\n' + ' ' * i + '0'

            while k + 1 < len(strDividend) - 1 and strDividend[k + 1] == '0':
                subStr = strDividend[k + 1]
                i += 1
                k += 1
        else:
            if int(subStr) // divider != 0 or k == len(strDividend) - 1:

                ans += '\n' + ' ' * i + subStr

                if int(subStr) <= divider:
                    return ans

                ans += '\n' + ' ' * i + str((int(subStr) // divider) * divider)
                subStr = str(int(subStr) - (int(subStr) // divider) * divider)
                i = k - len(subStr) + 1

                if k == len(strDividend) - 1:
                    break
            else:
                k += 1
                subStr += strDividend[k]

    return ans + '\n' + ' ' * (k - len(subStr) + 1) + subStr


def main():
    my_file = open("OUTPUT.txt", "w+")
    my_file.write(long_division(123, 123)+'\n'+'\n')
    my_file.write(long_division(1, 1)+'\n'+'\n')
    my_file.write(long_division(15, 3)+'\n'+'\n')
    my_file.write(long_division(3, 15)+'\n'+'\n')
    my_file.write(long_division(12345, 25)+'\n'+'\n')
    my_file.write(long_division(1234, 1423)+'\n'+'\n')
    my_file.write(long_division(87654532, 1)+'\n'+'\n')
    my_file.write(long_division(24600, 123)+'\n'+'\n')
    my_file.write(long_division(100000, 50)+'\n'+'\n')
    my_file.write(long_division(123456789, 531)+'\n'+'\n')
    my_file.write(long_division(425934261694251, 12345678)+'\n'+'\n')
    my_file.close()


if __name__ == '__main__':
    main()