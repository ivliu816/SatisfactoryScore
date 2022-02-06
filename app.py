from flask import Flask, request
import pandas as pd
import sqlite3 
app = Flask(__name__)

@app.route('/getRecipeInfo')
def getRecipeInfo():
    con = sqlite3.connect('./database/susresults.db')
    cur = con.cursor()
    recipe = request.args.get('recipe')
    x = cur.execute("SELECT * FROM susresults WHERE RECIPE='{}'".format("Scrambled Eggs")).fetchone()
    con.close()
    return x

@app.route('/getRecipes')
def getRecipeList():
    location = request.args.get('location')
    time = request.args.get('time')

# The above function returns the HTML code to be displayed on the page

if __name__ == '__main__':

   app.run()