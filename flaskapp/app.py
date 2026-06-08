from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Student Portal</title>
        <style>
            body{
                font-family: Arial;
                background-color: #f2f2f2;
                text-align:center;
                padding-top:100px;
            }
            .box{
                background:white;
                width:400px;
                margin:auto;
                padding:30px;
                border-radius:10px;
                box-shadow:0 0 10px gray;
            }
            h1{
                color:#2c3e50;
            }
            p{
                color:#555;
            }
            button{
                padding:10px 20px;
                background:#3498db;
                color:white;
                border:none;
                border-radius:5px;
            }
        </style>
    </head>

    <body>
        <div class="box">
            <h1>Welcome to AWS EC2</h1>
            <p>Flask Application Successfully Deployed</p>
            <button>Student Dashboard</button>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
