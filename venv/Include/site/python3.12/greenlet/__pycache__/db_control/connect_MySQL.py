from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# データベース接続情報
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# MySQLのURL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SSL証明書ファイルのパスを環境変数から取得
SSL_CA_PATH = os.getenv('SSL_CA_PATH')

# SSL証明書ファイルのパスを絶対パスに変換
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)  # db_controlの親ディレクトリ（backend）
cert_path = os.path.join(backend_dir, "DigiCertGlobalRootG2.crt.pem")
print(f"証明書パス: {cert_path}")
print(f"ファイル存在確認: {os.path.exists(cert_path)}")

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": cert_path,
            "check_hostname": False
        }
    }
)
