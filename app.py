# backend/app.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from db_control import crud, mymodels_MySQL
# MySQLのテーブル作成
from db_control.create_tables_MySQL import init_db
# アプリケーション初期化時にテーブルを作成
init_db()

# Pydanticモデルの定義
class Customer(BaseModel):
    customer_id: str
    customer_name: str
    age: int
    gender: str

# FastAPIアプリケーションの作成
app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルートエンドポイント
@app.get("/")
def index():
    return {"message": "FastAPI top page!"}

# 顧客作成エンドポイント
@app.post("/customers")
def create_customer(customer: Customer):
    # ✅ バリデーション：customer_id が空でないか確認
    if not customer.customer_id or customer.customer_id.strip() == "":
        raise HTTPException(status_code=400, detail="customer_id は必須です")

    # ✅ バリデーション：customer_name が空でないか確認
    if not customer.customer_name or customer.customer_name.strip() == "":
        raise HTTPException(status_code=400, detail="customer_name は必須です")

    # ✅ バリデーション：age が有効か確認
    if customer.age is None or customer.age <= 0:
        raise HTTPException(status_code=400, detail="age は正の数値で入力してください")

    # ✅ バリデーション：gender が空でないか確認
    if not customer.gender or customer.gender.strip() == "":
        raise HTTPException(status_code=400, detail="gender は必須です")

    # ✅ すべてのバリデーションを通過したら、データを挿入
    values = customer.dict()
    tmp = crud.myinsert(mymodels_MySQL.Customers, values)
    result = crud.myselect(mymodels_MySQL.Customers, values.get("customer_id"))

    if result:
        result_obj = json.loads(result)
        return result_obj if result_obj else None
    return None

# 顧客取得エンドポイント
@app.get("/customers")
def read_one_customer(customer_id: str = Query(...)):
    result = crud.myselect(mymodels_MySQL.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

# 全顧客取得エンドポイント
@app.get("/allcustomers")
def read_all_customer():
    result = crud.myselectAll(mymodels_MySQL.Customers)
    # 結果がNoneの場合は空配列を返す
    if not result:
        return []
    # JSON文字列をPythonオブジェクトに変換
    return json.loads(result)

# 顧客更新エンドポイント
@app.put("/customers")
def update_customer(customer: Customer):
    values = customer.dict()
    values_original = values.copy()
    tmp = crud.myupdate(mymodels_MySQL.Customers, values)
    result = crud.myselect(mymodels_MySQL.Customers, values_original.get("customer_id"))
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

# 顧客削除エンドポイント
@app.delete("/customers")
def delete_customer(customer_id: str = Query(...)):
    result = crud.mydelete(mymodels_MySQL.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"customer_id": customer_id, "status": "deleted"}

# テスト用エンドポイント
@app.get("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json()
