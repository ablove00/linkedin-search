# LinkedIn Dataset Search Engine

## معرفی پروژه

این پروژه یک وب‌اپلیکیشن ساده برای جستجو و فیلتر اطلاعات کاربران لینکدین
است که تمرکز آن بر منطق جستجو، ساختار بک‌اند و ارتباط بین فرانت‌اند و
بک‌اند می‌باشد. موتور جستجو با استفاده از Elasticsearch پیاده‌سازی شده و
APIها با FastAPI توسعه داده شده‌اند.

------------------------------------------------------------------------

## بررسی و پاکسازی داده‌ها

### منبع داده

داده‌های اولیه از فایل زیر بارگذاری شده‌اند:

`300-user-linkedin.txt`

### مشکلات داده اولیه

داده خام شامل مقادیر نامعتبر، تکراری و نویز بالا بوده است. به همین دلیل
عملیات پاکسازی داده انجام شد.

### آمار داده‌ها

-   Rows data: 337\
-   Rows before deduplication: 295\
-   Rows after deduplication: 260\
-   Removed rows: 77

### پاکسازی داده

عملیات پاکسازی از طریق اسکریپت `export_text.py` انجام شده و فقط روی
ستون‌های زیر اعمال شده است:

-   full_name
-   job_title
-   industry
-   summary
-   location_country
-   education
-   experience
-   skills
-   job_summary

------------------------------------------------------------------------

## راه‌اندازی Elasticsearch با Docker

``` bash
docker run -d --name es -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.11.1
```

تست اجرا:

    http://localhost:9200

------------------------------------------------------------------------

## Backend (FastAPI)

### نصب وابستگی‌ها

``` bash
pip install -r requirements.txt
```

### ایندکس داده‌ها

``` bash
py ingest_data.py
```

### اجرای سرور

``` bash
py uvicorn main:app --reload --port 8021
```

------------------------------------------------------------------------

## APIهای جستجو

### جستجوی ساده (OR-based)

Endpoint: `GET /search`

-   جستجو همزمان روی چند ستون
-   استفاده از یک Query واحد
-   شرط OR بین ستون‌ها

### جستجوی پیشرفته (AND-based)

Endpoint: `POST /search/advanced`

-   هر فیلد اختیاری است
-   شرط AND بین فیلدهای ارسال‌شده
-   دقت بالاتر در نتایج

------------------------------------------------------------------------

## Frontend (React)

### راه‌اندازی

``` bash
npx create-react-app frontend
cd frontend
npm install bootstrap react-bootstrap
npm install react-router-dom
npm start
```

### صفحات طراحی‌شده

-   صفحه جستجوی ساده متصل به `/search`
-   صفحه جستجوی پیشرفته متصل به `/search/advanced`

------------------------------------------------------------------------

## تکنولوژی‌ها

-   Python
-   FastAPI
-   Elasticsearch
-   Docker
-   React
-   Bootstrap
