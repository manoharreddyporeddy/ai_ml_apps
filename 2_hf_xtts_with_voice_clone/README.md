```batch

..\myenv311\Scripts\activate
python.exe -m pip install --upgrade pip

REM =========== USER ===========
pip install -r requirements.txt

REM =========== DEV ===========
REM pip install gradio_client ffmpeg-python
REM pip freeze > requirements.txt

```
