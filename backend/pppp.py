# מקור התווים שמהם נבנה ה-Buffer (כפי שזיהינו מהקוד שלך)
SOURCE = "0123456789ABCDEF" * 2  # לפי האורך שראיתי, כנראה מוכפל

# נבנה את ה־buffer בדומה ללולאה שפורסה
buffer = []
var_2AC = 0  # מתחיל מ־0
target_length = 0x29  # 41 תווים

while len(buffer) < target_length:
    char = SOURCE[var_2AC % len(SOURCE)]
    buffer.append(char)
    
    # חיקוי של הקוד הזה:
    # add     ecx, 1
    # and     ecx, 80000003h
    # jns     short loc_4016BD
    var_2AC = (var_2AC + 1) & 0x80000003
    if var_2AC & 0x80000000:
        break  # הסימן שלילי, יוצאים מהלולאה

buffer_str = ''.join(buffer)
print("Buffer constructed:", buffer_str)
