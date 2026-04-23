from flask import Flask, request, render_template_string
from blockchain import Blockchain
from hasher import safe_compare

app = Flask(__name__)
chain = Blockchain()


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CipherChain Viewer</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            padding: 30px;
        }

        h1 {
            text-align: center;
            color: #22c55e;
            margin-bottom: 10px;
        }

        h2 {
            color: #38bdf8;
            margin-top: 30px;
        }

        .container {
            max-width: 900px;
            margin: auto;
        }

        .block {
            background: #1e293b;
            border-radius: 10px;
            padding: 15px;
            margin: 12px 0;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            transition: 0.2s;
        }

        .block:hover {
            transform: scale(1.02);
        }

        .label {
            color: #94a3b8;
        }

        .value {
            color: #f8fafc;
            word-break: break-all;
        }

        .form-box {
            background: #1e293b;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }

        input {
            width: 100%;
            padding: 12px;
            border-radius: 6px;
            border: none;
            margin-bottom: 10px;
            font-size: 14px;
        }

        button {
            width: 100%;
            padding: 12px;
            background: #22c55e;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #16a34a;
        }

        .result {
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
        }

        .success {
            background: #064e3b;
            color: #22c55e;
        }

        .fail {
            background: #450a0a;
            color: #ef4444;
        }
    </style>
</head>
<body>

<div class="container">

<h1>🔗 CipherChain</h1>
<p style="text-align:center; color:#94a3b8;">
Decentralized Document Verification
</p>

<h2>📦 Blockchain Ledger</h2>

{% for block in chain %}
<div class="block">
    <div><span class="label">Block #:</span> <span class="value">{{block.index}}</span></div>
    <div><span class="label">Data:</span> <span class="value">{{block.data}}</span></div>
    <div><span class="label">Hash:</span> <span class="value">{{block.hash}}</span></div>
    <div><span class="label">Prev:</span> <span class="value">{{block.previous_hash}}</span></div>
</div>
{% endfor %}

<h2>🔍 Verify Document</h2>

<div class="form-box">
<form method="POST">
    <input name="hash" placeholder="Paste SHA-256 hash here" required>
    <button type="submit">Verify</button>
</form>

{% if result %}
<div class="result {{'success' if 'AUTHENTIC' in result else 'fail'}}">
    {{result}}
</div>
{% endif %}
</div>

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        user_hash = request.form["hash"]

        block = chain.find_hash(user_hash)

        if block and safe_compare(user_hash, block.data):
            result = "✅ AUTHENTIC — Hash found on blockchain"
        else:
            result = "❌ NOT AUTHENTIC — No match found"

    return render_template_string(HTML, chain=chain.chain, result=result)


if __name__ == "__main__":
    app.run(debug=True)