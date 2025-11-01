# Quick Start Guide - Hướng Dẫn Nhanh

Hướng dẫn nhanh để chạy hệ thống JWT Authentication với RSA trong 5 phút.

## 🚀 Chọn Phương Thức

### 🐳 Cách 1: Docker (Nhanh nhất - Khuyên dùng)

**Yêu cầu:** Docker và Docker Compose đã cài đặt

```bash
# 1. Tạo RSA keys (cần Python)
python generate_keys.py

# 2. Chạy tất cả services
docker-compose up --build
```

**Xong!** Services sẽ chạy tại:
- **Auth Service:** http://localhost:8000/docs
- **Resource Service:** http://localhost:8001/docs
- **Frontend Demo:** Mở `front_end/index.html` trong browser

---

### 💻 Cách 2: Local Development (với venv)

## ⚡ Các Bước Chạy Nhanh

### Bước 1: Tạo Virtual Environment

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
# Nếu lỗi: Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

**Windows CMD:**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Bước 2: Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Tạo RSA Keys

```bash
python generate_keys.py
```

### Bước 4: Chạy Services

**Terminal 1 - Auth Service:**
```bash
cd auth_service
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Resource Service:**
```bash
cd resource_service
uvicorn app.main:app --reload --port 8001
```

### Bước 5: Test

**Option 1: Dùng Frontend Demo (Khuyên dùng)**
- Mở file `front_end/index.html` trong browser
- Test các chức năng: Đăng ký → Đăng nhập → Xem sản phẩm

**Option 2: Dùng API trực tiếp**

**1. Đăng ký user:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "test123456"}'
```

**2. Đăng nhập:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "test123456"}'
```

Copy `access_token` từ response.

**3. Lấy danh sách sản phẩm:**
```bash
curl -X GET "http://localhost:8001/api/products" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

## ✅ Kiểm Tra Nhanh

**Health check:**
```bash
curl http://localhost:8000/health  # Auth Service
curl http://localhost:8001/health  # Resource Service
```

**API Documentation (Swagger UI):**
- Auth Service: http://localhost:8000/docs
- Resource Service: http://localhost:8001/docs

## 🎯 Tính Năng

- ✅ Đăng ký user mới
- ✅ Đăng nhập và nhận JWT token (RS256 với RSA)
- ✅ Xem danh sách sản phẩm (cần JWT token)
- ✅ Frontend demo đầy đủ chức năng

## 🐛 Lỗi Thường Gặp

1. **"Private key not found"** → Chạy `python generate_keys.py`
2. **"Module not found"** → Chạy `pip install -r requirements.txt`
3. **"Port already in use"** → Đổi port hoặc kill process đang dùng port đó
4. **PowerShell Execution Policy** → Dùng `.\activate_venv.ps1` hoặc CMD

## 📚 Xem Thêm

- Chi tiết đầy đủ: [DEPLOYMENT.md](./DEPLOYMENT.md)
- Tổng quan dự án: [README.md](./README.md)
