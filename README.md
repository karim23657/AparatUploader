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
ap.upload(
    videopath='Yersinia enterobacterica.mp4',
    title="عنوان فیلم",
    description='''توضیحات''',
    progress_callback=print
)
```
