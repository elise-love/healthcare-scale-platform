##Project Structure🌷🌷🌷
```
scale_platform/
├─ app/
│  ├─ main.py                 #FastAPI 入口
│  ├─ core/
│  │  ├─ config.py          
│  │  └─ db.py              
│  ├─ models/
│  │  ├─ scale.py           
│  │  └─ response.py       
│  ├─ schemas/             
│  ├─ services/
│  │  ├─ scoring.py           
│  │  └─ scale_loader.py    
│  ├─ routers/
│  │  ├─ pages.py           
│  │  └─ api.py        
│  ├─ templates/              #Jinja2 HTML
│  │  ├─ base.html
│  │  ├─ fill_scale.html
│  │  └─ history.html
│  └─ static/               
│     └─ style.css
├─ scales/                    #量表定義檔（JSON）
│  └─ example_scale.json
├─ tests/
├─ .env                      
├─ .gitignore
├─ requirements.txt
└─ README.md
```