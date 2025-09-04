import cloudinary
import cloudinary.uploader

cloudinary.config(
  cloud_name = 'ddephsl2g',
  api_key = '767532485926878',
  api_secret = 'VREodp8Mrgs4IFIBwfbD28TTBgY'
)

# כאן תעלי תמונה או תשתמשי ב-API
result = cloudinary.uploader.upload("C:/Users/מיכל מילר/Downloads/How I Repaired My Nails & Renewed My Skin — My Simple Inside-Out Solution.jpg")
print(result["secure_url"])  # כתובת התמונה בענן
result2 = cloudinary.uploader.upload("C:/Users/מיכל מילר/Downloads/Business Finance Bar Profit Vector illustration stock illustration #finance #financebargraph #financial #profitgraph #economy #financearrow #growth #business #logo #drawing #outline #silhouette #clipart #cute #.jpg")
print(result2["secure_url"])   # כתובת התמונה בענן