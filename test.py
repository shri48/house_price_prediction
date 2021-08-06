from flask import Flask,render_template,jsonify,request

app = Flask(__name__)

@app.route('/')  # Default API
def home():
    return render_template("new.html")

@app.route('/print', methods=["POST","GET"])
def user_info_print():
    
    sqft = request.form.get("user_name")
    print(f"{sqft=}")
    return render_template("new2.html")

if __name__ =="__main__":
    app.run()

