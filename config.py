DB_CONFIG = {
    "host": "fmcg-project.mysql.database.azure.com",
    "user": "Mohamedali26",
    "password": "Mo#12321",
    "database": "fmcg_project",
    "ssl_ca": r"E:\Mohamed\Data Analyst\dash_ai_dashboard\assets\ssl\DigiCertGlobalRootCA.pem"
}


connection_str = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}?"
    f"ssl_ca={DB_CONFIG['ssl_ca']}"
)