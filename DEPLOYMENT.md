# Hướng Dẫn Deploy Hệ Thống JWT Authentication với RSA

Hệ thống demo xác thực JWT sử dụng RSA (bất đối xứng) với 2 services:
- **Auth Service** (Port 8000): Đăng ký, đăng nhập, tạo JWT token
- **Resource Service** (Port 8001): API Products với JWT authentication

## 🚀 Phương Thức Deploy

Có 2 cách để chạy project:

### 1. 🐳 Docker (Deployment/Production) - Khuyên dùng

- **Ưu điểm:** 
  - Môi trường nhất quán, dễ deploy
  - Tự động cài đặt dependencies
  - Không cần venv
  - Phù hợp production

### 2. 💻 Local Development (với venv)

- **Ưu điểm:**
  - Nhanh cho development
  - Dễ debug
  - Hot reload
  - Phù hợp development/testing

## 📋 Yêu Cầu Hệ Thống

### Cho Docker:
- Docker và Docker Compose
- Git (nếu clone từ repository)

### Cho Local Development:
- Python 3.8 trở lên
- pip (Python package manager)
- Git (nếu clone từ repository)

## 🐳 PHƯƠNG THỨC 1: Deploy với Docker

### Bước 1: Tạo RSA Keys (nếu chưa có)

```bash
# Cần Python để chạy script tạo keys
python generate_keys.py
```

Hoặc tạo keys trong Docker container sau khi chạy services.

### Bước 2: Build và Chạy với Docker Compose

```bash
# Build và chạy tất cả services
docker-compose up --build

# Hoặc chạy ở background
docker-compose up -d --build
```

### Bước 3: Kiểm Tra Services

- Auth Service: http://localhost:8000/docs
- Resource Service: http://localhost:8001/docs

### Bước 4: Dừng Services

```bash
# Dừng và xóa containers
docker-compose down

# Dừng và xóa containers + volumes (xóa cả database)
docker-compose down -v
```

**Lưu ý:** 
- Docker sẽ tự động mount volumes cho code và database
- Thay đổi code sẽ tự động reload (nhờ volume mount)
- Database được lưu tại `./data/`

---

## 💻 PHƯƠNG THỨC 2: Local Development với venv

## 🚀 Bước 1: Chuẩn Bị Môi Trường

### 1.1. Tạo Virtual Environment (Khuyên dùng)

**Windows PowerShell:**

Tạo venv:
```powershell
python -m venv venv
```

Kích hoạt venv (nếu gặp lỗi Execution Policy):

**Cách 1: Bypass Execution Policy (Khuyên dùng)**
```powershell
.\venv\Scripts\Activate.ps1
```

**Cách 2: Set Execution Policy cho Current User**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**Cách 3: Dùng Command Prompt thay vì PowerShell**
```cmd
venv\Scripts\activate.bat
```

**Kiểm tra venv đã được kích hoạt:**
```powershell
python --version
$env:VIRTUAL_ENV  # Sẽ hiển thị đường dẫn đến venv nếu đã activate
```

**Windows Command Prompt (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 1.2. Cài Đặt Dependencies

Từ thư mục gốc của project:
```bash
pip install -r requirements.txt
```

Hoặc cài đặt riêng cho từng service:

**Auth Service:**
```bash
cd auth_service
pip install -r requirements.txt
cd ..
```

**Resource Service:**
```bash
cd resource_service
pip install -r requirements.txt
cd ..
```

## 🔑 Bước 2: Tạo RSA Keys

RSA keys cần thiết cho việc ký (sign) và xác thực (verify) JWT tokens.

### 2.1. Chạy Script Tạo Keys

Từ thư mục gốc:
```bash
python generate_keys.py
```

Script này sẽ:
- Tạo cặp khóa RSA (2048-bit)
- Lưu `private.pem` vào `auth_service/rsa_keys/`
- Lưu `public.pem` vào `auth_service/rsa_keys/`
- Copy `public.pem` vào `resource_service/rsa_keys/`

### 2.2. Kiểm Tra Keys Đã Được Tạo

Đảm bảo các file sau tồn tại:
- ✅ `auth_service/rsa_keys/private.pem`
- ✅ `auth_service/rsa_keys/public.pem`
- ✅ `resource_service/rsa_keys/public.pem`

## 💾 Bước 3: Khởi Tạo Database

### 3.1. Khởi Tạo Database cho Auth Service

Khi chạy Auth Service lần đầu, database sẽ tự động được tạo và khởi tạo:

```bash
cd auth_service
python -m uvicorn app.main:app --reload --port 8000
```

Database sẽ được tạo tại: `data/auth_service/auth_service.db`

**User mặc định được tạo:**
- Username: `admin`
- Password: `admin123`

### 3.2. Khởi Tạo Database cho Resource Service

Tương tự, khi chạy Resource Service lần đầu:

```bash
cd resource_service
python -m uvicorn app.main:app --reload --port 8001
```

Database sẽ được tạo tại: `data/resource_service/resource_service.db`

**Dữ liệu mẫu:**
- Tự động tạo 4 sản phẩm mẫu để test

## 🏃 Bước 4: Chạy Services

**Terminal 1 - Auth Service:**
```bash
cd auth_service
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Resource Service:**
```bash
cd resource_service
python -m uvicorn app.main:app --reload --port 8001
```

## ✅ Bước 5: Kiểm Tra Services Đang Chạy

### 5.1. Health Check

**Auth Service:**
```bash
curl http://localhost:8000/health
```
Response: `{"status": "healthy", "service": "auth_service"}`

**Resource Service:**
```bash
curl http://localhost:8001/health
```
Response: `{"status": "healthy", "service": "resource_service"}`

### 5.2. Truy Cập API Documentation

- **Auth Service Swagger UI:** http://localhost:8000/docs
- **Resource Service Swagger UI:** http://localhost:8001/docs

## 🧪 Bước 6: Test API

### 6.1. Đăng Ký User Mới

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123456"
  }'
```

Response mẫu:
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00"
}
```

### 6.2. Đăng Nhập và Lấy JWT Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test123456"
  }'
```

Response mẫu:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Lưu ý:** Lưu lại `access_token` để dùng cho các request tiếp theo.

### 6.3. Lấy Danh Sách Sản Phẩm (Cần JWT)

```bash
curl -X GET "http://localhost:8001/api/products?page=1&size=10" \
  -H "Authorization: Bearer <access_token>"
```

Thay `<access_token>` bằng token đã nhận ở bước 6.2.

Response mẫu:
```json
{
  "products": [
    {
      "id": 1,
      "name": "Laptop Gaming",
      "description": "Laptop gaming cao cấp với card đồ họa RTX 4060",
      "price": 25000000.0,
      "category": "Electronics",
      "stock_quantity": 10,
      "is_active": true,
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 4,
  "page": 1,
  "size": 10
}
```

### 6.4. Test Với Token Không Hợp Lệ

```bash
curl -X GET "http://localhost:8001/api/products" \
  -H "Authorization: Bearer invalid_token"
```

Response: `401 Unauthorized` với message lỗi.

## 📝 Bước 7: Cấu Hình Nâng Cao (Optional)

### 7.1. Thay Đổi Cấu Hình JWT

Chỉnh sửa file `auth_service/app/core/config.py`:

```python
# Thời gian hết hạn token (phút)
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Thay đổi giá trị này
```

### 7.2. Thay Đổi Cấu Hình CORS

Nếu cần kết nối từ frontend khác:

Chỉnh sửa `auth_service/app/core/config.py`:
```python
ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8001", "http://your-frontend-domain"]
```

### 7.3. Sử Dụng Environment Variables

Tạo file `.env` ở thư mục gốc:

```env
# Auth Service
DATABASE_URL=sqlite:///./data/auth_service.db
PRIVATE_KEY_PATH=rsa_keys/private.pem
PUBLIC_KEY_PATH=rsa_keys/public.pem
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Resource Service
DATABASE_URL=sqlite:///./data/resource_service.db
PUBLIC_KEY_PATH=rsa_keys/public.pem
```

## 🐛 Troubleshooting

### Lỗi: "Cannot be loaded because running scripts is disabled" (Windows PowerShell)

**Nguyên nhân:** PowerShell Execution Policy chặn việc chạy scripts.

**Giải pháp:**

**Cách 1: Bypass trực tiếp (Khuyên dùng)**
```powershell
.\venv\Scripts\Activate.ps1
```
Nếu vẫn lỗi, thử:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\venv\Scripts\Activate.ps1
```

**Cách 2: Set Execution Policy cho Current User**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**Cách 3: Dùng Command Prompt (CMD) thay vì PowerShell**
```cmd
venv\Scripts\activate.bat
```

**Cách 4: Dùng Git Bash hoặc WSL**
```bash
source venv/Scripts/activate  # Git Bash
# hoặc
source venv/bin/activate      # WSL
```

### Lỗi: "Private key not found"
- **Nguyên nhân:** Chưa chạy `generate_keys.py`
- **Giải pháp:** Chạy `python generate_keys.py`

### Lỗi: "ModuleNotFoundError: No module named 'xxx'"
- **Nguyên nhân:** Chưa cài đặt dependencies
- **Giải pháp:** `pip install -r requirements.txt`

### Lỗi: "Cannot connect to database"
- **Nguyên nhân:** Đường dẫn database không đúng hoặc không có quyền ghi
- **Giải pháp:** Kiểm tra đường dẫn trong `config.py` và đảm bảo thư mục `data/` tồn tại

### Lỗi: "Token không hợp lệ" khi gọi Resource Service
- **Nguyên nhân:** 
  - Token đã hết hạn
  - Public key không khớp với private key
  - Token không đúng format
- **Giải pháp:**
  - Đăng nhập lại để lấy token mới
  - Đảm bảo public key trong `resource_service/rsa_keys/` khớp với auth service
  - Kiểm tra token format (phải bắt đầu bằng `Bearer `)

### Lỗi: "Port already in use"
- **Nguyên nhân:** Port 8000 hoặc 8001 đang được sử dụng
- **Giải pháp:** 
  - Đổi port trong lệnh uvicorn: `--port 8002`
  - Hoặc kill process đang dùng port đó

## 📚 Tài Liệu Tham Khảo

- **FastAPI:** https://fastapi.tiangolo.com/
- **JWT với RSA:** https://pyjwt.readthedocs.io/
- **Python-jose:** https://python-jose.readthedocs.io/
- **SQLAlchemy:** https://docs.sqlalchemy.org/

## 🎯 Tóm Tắt Quy Trình

1. ✅ Cài đặt Python và dependencies
2. ✅ Tạo RSA keys (`python generate_keys.py`)
3. ✅ Chạy Auth Service (port 8000)
4. ✅ Chạy Resource Service (port 8001)
5. ✅ Test đăng ký/đăng nhập
6. ✅ Test API products với JWT token

## 📞 Liên Hệ

Nếu gặp vấn đề, vui lòng kiểm tra:
- Logs của services
- Database đã được tạo chưa
- RSA keys đã được tạo đúng chưa
- Port có bị conflict không

