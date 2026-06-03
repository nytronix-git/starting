from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Simple Calculator", version="1.0.0")

# Request/Response models
class CalcRequest(BaseModel):
    a: float
    b: float

class CalcResponse(BaseModel):
    result: float
    operation: str

# HTML UI
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Calculator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            padding: 40px;
            max-width: 500px;
            width: 100%;
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2em;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
            font-size: 0.95em;
        }
        
        input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .button-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        button {
            padding: 12px 20px;
            font-size: 0.95em;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            color: white;
        }
        
        .btn-operation {
            background-color: #667eea;
        }
        
        .btn-operation:hover {
            background-color: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-clear {
            grid-column: 1 / -1;
            background-color: #ff6b6b;
        }
        
        .btn-clear:hover {
            background-color: #ee5a52;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }
        
        .result-box {
            background: #f8f9fa;
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            min-height: 60px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .result-label {
            color: #888;
            font-size: 0.85em;
            margin-bottom: 5px;
        }
        
        .result-value {
            color: #333;
            font-size: 2em;
            font-weight: bold;
        }
        
        .error {
            color: #ff6b6b;
        }
        
        .success {
            color: #51cf66;
        }
        
        .operation-name {
            color: #667eea;
            font-size: 0.9em;
            margin-top: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧮 Calculator</h1>
        
        <div class="input-group">
            <label for="num1">First Number</label>
            <input type="number" id="num1" placeholder="Enter first number" step="any">
        </div>
        
        <div class="input-group">
            <label for="num2">Second Number</label>
            <input type="number" id="num2" placeholder="Enter second number" step="any">
        </div>
        
        <div class="button-grid">
            <button class="btn-operation" onclick="calculate('add')">➕ Adddddd</button>
            <button class="btn-operation" onclick="calculate('subtract')">➖ Subtract</button>
            <button class="btn-operation" onclick="calculate('multiply')">✖️ Multiply</button>
            <button class="btn-operation" onclick="calculate('divide')">➗ Divide</button>
            <button class="btn-operation" onclick="calculate('power')">🔋 Power</button>
            <button class="btn-operation" onclick="calculate('modulo')">📊 Modulo</button>
            <button class="btn-clear" onclick="clearFields()">Clear</button>
        </div>
        
        <div class="result-box" id="result">
            <div class="result-label">Result</div>
            <div class="result-value">-</div>
        </div>
    </div>
    
    <script>
        async function calculate(operation) {
            const num1 = parseFloat(document.getElementById('num1').value);
            const num2 = parseFloat(document.getElementById('num2').value);
            const resultBox = document.getElementById('result');
            
            if (isNaN(num1) || isNaN(num2)) {
                resultBox.innerHTML = '<div class="result-label">Error</div><div class="result-value error">Please enter valid numbers</div>';
                return;
            }
            
            try {
                const response = await fetch(`/${operation}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ a: num1, b: num2 })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    resultBox.innerHTML = `
                        <div class="result-label">Result</div>
                        <div class="result-value success">${data.result}</div>
                        <div class="operation-name">${data.operation}</div>
                    `;
                } else {
                    resultBox.innerHTML = `<div class="result-label">Error</div><div class="result-value error">${data.detail}</div>`;
                }
            } catch (error) {
                resultBox.innerHTML = `<div class="result-label">Error</div><div class="result-value error">Connection failed</div>`;
            }
        }
        
        function clearFields() {
            document.getElementById('num1').value = '';
            document.getElementById('num2').value = '';
            document.getElementById('result').innerHTML = '<div class="result-label">Result</div><div class="result-value">-</div>';
            document.getElementById('num1').focus();
        }
        
        // Allow Enter key to calculate
        document.getElementById('num1').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') document.getElementById('num2').focus();
        });
        document.getElementById('num2').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') calculate('add');
        });
    </script>
</body>
</html>
"""

# Serve the UI
@app.get("/", tags=["root"], response_class=HTMLResponse)
def read_root():
    """Serve the calculator UI"""
    return HTML_CONTENT

@app.post("/add", response_model=CalcResponse, tags=["operations"])
def add(request: CalcRequest):
    """Add two numbers"""
    return {"result": request.a + request.b, "operation": "addition"}

@app.post("/subtract", response_model=CalcResponse, tags=["operations"])
def subtract(request: CalcRequest):
    """Subtract two numbers"""
    return {"result": request.a - request.b, "operation": "subtraction"}

@app.post("/multiply", response_model=CalcResponse, tags=["operations"])
def multiply(request: CalcRequest):
    """Multiply two numbers"""
    return {"result": request.a * request.b, "operation": "multiplication"}

@app.post("/divide", response_model=CalcResponse, tags=["operations"])
def divide(request: CalcRequest):
    """Divide two numbers"""
    if request.b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": request.a / request.b, "operation": "division"}

@app.post("/power", response_model=CalcResponse, tags=["operations"])
def power(request: CalcRequest):
    """Raise a to the power of b"""
    return {"result": request.a ** request.b, "operation": "power"}

@app.post("/modulo", response_model=CalcResponse, tags=["operations"])
def modulo(request: CalcRequest):
    """Get remainder of a divided by b"""
    if request.b == 0:
        raise HTTPException(status_code=400, detail="Cannot modulo by zero")
    return {"result": request.a % request.b, "operation": "modulo"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
