
from flask import Flask, request, render_template_string, send_file
import io

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
<title>Smart Event Seating Planner</title>
<style>
body{font-family:Arial;background:#f4f4f4;padding:30px}
.container{max-width:900px;margin:auto;background:#fff;padding:20px;border-radius:10px}
textarea,input{width:100%;padding:8px;margin:8px 0}
table{border-collapse:collapse;width:100%;margin-top:20px}
th,td{border:1px solid #ccc;padding:8px;text-align:center}
button{padding:10px 20px}
</style>
</head>
<body>
<div class="container">
<h2>Smart Event Seating Planner</h2>
<p>Upload TXT or paste guest data.</p>
<form method="post" enctype="multipart/form-data">
<label>Tables</label>
<input type="number" name="tables" value="3" min="1">
<label>Seats per Table</label>
<input type="number" name="capacity" value="4" min="1">
<label>Upload TXT</label>
<input type="file" name="file">
<label>OR Paste Data</label>
<textarea name="data" rows="8">#GuestName,Group,VIP,Friends,Avoid
Alice,Family,Yes,Bob|Charlie,David
Bob,Family,No,Alice,
Charlie,Office,No,Alice,Eve
David,Office,Yes,,Alice
Eve,Friends,No,,Charlie
Frank,Friends,No,Grace,
Grace,Friends,No,Frank,
</textarea>
<button type="submit">Generate Seating</button>
</form>
{% if seating %}
<h3>Seating Plan</h3>
<table>
<tr>{% for i in range(seating|length) %}<th>Table {{i+1}}</th>{% endfor %}</tr>
<tr>
{% for t in seating %}
<td>{% for g in t %}{{g}}<br>{% endfor %}</td>
{% endfor %}
</tr>
</table>
<form action="/download" method="post">
<input type="hidden" name="content" value="{{text}}">
<button>Download Seating Plan</button>
</form>
{% endif %}
</div>
</body>
</html>
"""

def parse(txt):
    guests=[]
    for line in txt.splitlines():
        line=line.strip()
        if not line or line.startswith("#"): continue
        p=[x.strip() for x in line.split(",")]
        while len(p)<5: p.append("")
        guests.append({
            "name":p[0],
            "group":p[1],
            "vip":p[2].lower()=="yes",
            "friends":[x for x in p[3].split("|") if x],
            "avoid":[x for x in p[4].split("|") if x]
        })
    return guests

def generate(guests,tables,cap):
    seating=[[] for _ in range(tables)]
    placed=set()

    def can_place(g,idx):
        if len(seating[idx])>=cap: return False
        for n in seating[idx]:
            og=next(x for x in guests if x["name"]==n)
            if og["name"] in g["avoid"] or g["name"] in og["avoid"]:
                return False
        return True

    # VIP first
    for g in [x for x in guests if x["vip"]]:
        for i in range(tables):
            if can_place(g,i):
                seating[i].append(g["name"])
                placed.add(g["name"])
                break

    # Friends together
    for g in guests:
        if g["name"] in placed: continue
        done=False
        for i in range(tables):
            if can_place(g,i):
                if not g["friends"]:
                    seating[i].append(g["name"]); placed.add(g["name"]); done=True; break
                # try existing friend table
                for f in g["friends"]:
                    if f in placed:
                        for ti,t in enumerate(seating):
                            if f in t and can_place(g,ti):
                                seating[ti].append(g["name"]); placed.add(g["name"]); done=True; break
                        if done: break
                if done: break
        if done: continue
        for i in range(tables):
            if can_place(g,i):
                seating[i].append(g["name"]); placed.add(g["name"]); break

    return seating

@app.route("/",methods=["GET","POST"])
def home():
    seating=None
    text=""
    if request.method=="POST":
        tables=int(request.form["tables"])
        cap=int(request.form["capacity"])
        if request.files["file"] and request.files["file"].filename:
            data=request.files["file"].read().decode()
        else:
            data=request.form["data"]
        guests=parse(data)
        seating=generate(guests,tables,cap)
        out=[]
        for i,t in enumerate(seating,1):
            out.append(f"Table {i}")
            out.extend(t)
            out.append("")
        text="\n".join(out)
    return render_template_string(HTML,seating=seating,text=text)

@app.route("/download",methods=["POST"])
def download():
    buf=io.BytesIO(request.form["content"].encode())
    return send_file(buf,as_attachment=True,download_name="seating_plan.txt",mimetype="text/plain")

if __name__=="__main__":
    app.run(debug=True)
