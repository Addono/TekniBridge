# ledstripTeknikringen

## Development
Create a virtual environment:
```bash
pip install virtualenv
```

Create a virtual Python environment
```bash
virtualenv venv
```

Activate the virtual environment
```bash
source venv/bin/activate
```

Install all `pip` dependencies
```bash
pip install -r requirements.txt
```

Now the application can be started with
```bash
python src/led_strip.py
```

Or if you want to have the simulator enabled
```bash
SIMULATE=1 python src/led_strip.py
```