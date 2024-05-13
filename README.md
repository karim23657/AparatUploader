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


