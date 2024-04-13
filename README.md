# AparatUploader

# How to use 


clone repo : 

```shell
git clone https://github.com/karim23657/AparatUploader
```

You need `cookies.txt` from your aparat account (use cookies.txt browser extention) :
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
