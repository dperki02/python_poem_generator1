#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 17:50:10 2024

@author: dana-paulette
"""
import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


import logging
from flask_cors import CORS

logging.basicConfig(level=logging.ERROR)

app = Flask(__name__)
"CORS(app)  # Allow CORS for all routes (optional)"

# Set OpenAI API key securely

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_poem', methods=['POST'])
def generate_poem():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')

        if not prompt:
            return jsonify({'poem': 'Please provide a theme or subject for the poem.'}), 400

        response = client.chat.completions.create(model="gpt-4",
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Write a poem about {prompt}."}
        ],                                         
        max_tokens=150)

    # Access the response content properly
        poem = response.choices[0].message.content.strip()
        return jsonify({'poem': poem})
    except Exception as e:
        logging.error("Error generating poem", exc_info=True)
        return jsonify({'poem': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)

