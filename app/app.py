from flask import Flask, jsonify, request,Response
import json
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# 配置 OpenAI API 密钥
# openai.api_key = 'sk-pr'

@app.route('/scrape', methods=['GET'])
def scrape_data():
    url = 'https://fund.eastmoney.com/fund.html'  # 东方财富基金页面
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    funds = []
    # 示例抓取逻辑：根据实际情况调整
    for row in soup.select('#oTable tbody tr'):
        code = row.find('td',class_='bzdm').text
        fund_name_tag = soup.find('td', class_='tol')
        name =  fund_name_tag.a.text.strip()
        net_value = row.find('td', class_='dwjz black').text
        anav=row.find('td', class_='ljjz black').text
        funds.append({'code': code, 'name': name,  'nav': net_value,'anav':anav})
    return Response(json.dumps(funds, ensure_ascii=False), mimetype='application/json')
    
@app.route('/analyze', methods=['POST'])
def analyze_funds():
    data = request.json
    prompt = data.get('prompt', '')

    # 使用 OpenAI API 进行分析
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
        {
            "role": "user",
            "content": prompt,
        },
    ],
    )
    analysis = response.choices[0].message.content
    return jsonify({'analysis': analysis})

if __name__ == '__main__':
    app.run(debug=True)
