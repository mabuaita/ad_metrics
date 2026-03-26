from flask import Flask, request, jsonify
import json, requests
def POST_request():
#    with open("FILE PATH", "r") as data:
#        JSON_Body = data.read()
    URL = "http://ad_metric.swhagy.com:8777"
    JSON_Body = {"2026-12-23 10:23:45", "aid-aa3345453", "qid_453464453mm"}
    Body = list(JSON_Body)
    response = requests.post(url=URL, json=Body, headers={"Content-Type":"application/json"})
    assert response.status_code == 200

for i in range(100):
    POST_request()
