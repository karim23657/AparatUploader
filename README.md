# AparatUploader

# How to use 


clone repo : 

```shell
git clone https://github.com/karim23657/AparatUploader
```

You need `cookies.txt` from your aparat account ( use cookies.txt browser extention [github](https://github.com/hrdl-github/cookies-txt) , [firefox](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) , [chrome](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) - go to https://www.aparat.com/dashboard and then export cookies):
```python
from AparatUploader.aparat import AparatUploader
ap = AparatUploader('cookies.txt')

def display_prog(fileChunk,fraction_completed):
    template = '\rPercent complete: {:.1%}'
    print(template.format(fraction_completed), end='')

ap.upload(
    videopath='Yersinia enterobacterica.mp4',
    title="عنوان فیلم",
    description='''توضیحات''',
    progress_callback=display_prog
)
```

Advanced example :

```python
from AparatUploader.aparat import AparatUploader
ap = AparatUploader('cookies.txt')

def display_prog(fileChunk,fraction_completed):
    template = '\rPercent complete: {:.1%}'
    print(template.format(fraction_completed), end='')


video_path=r'C:\Users\Admin\Downloads\فیلم.mp4'
# srt - فایل زیر نویس
with open(r'C:\Users\Admin\Downloads\فیلم.srt',"r",encoding='utf8') as f:
    srt_formatted = f.read()


import base64
image_path = 'path/to/your/image.jpg'

with open(image_path, 'rb') as image_file:
    image_content = image_file.read()

# Convert image to base64
base64_thumbnail = base64.b64encode(image_content).decode()

# Construct data URL
thumbnail = f"data:image/jpeg;base64,{base64_thumbnail}"

ap.upload(
        video_path,
        title='عنوان مناسب',
        description='توضیحات فیلم',
        progress_callback=display_prog,
        tags='تگ1-تگ2-تگ3',   # tags - حتما بینشان '-' باشد - حداقل 3 تا
        category="3", # تحصیلات و یادگیری
        playlist="98985",
        playlistid=["98985"],
        subtitle=srt_formatted,
        thumbnail=thumbnail,
        # thumbnail-file="C:\\fakepath\\in99dex.jpg"
        video_pass='0',# share now
        video_subtitle_file="C:\\fakepath\\how_to.srt"
        
    )
```

